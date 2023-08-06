from typing import Union
from pathlib import Path
import requests
import pandas as pd
from datasetmaker.models import Client
from datasetmaker.datapackage import DataPackage
from datasetmaker.onto.manager import (
    sid_to_id,
    _map)

pd.options.mode.chained_assignment = None


country_name_to_id = _map(entity_name='country',
                          keys=['name', 'alt_name'],
                          value='country')


class NobelClient(Client):
    url = 'http://api.nobelprize.org/v1/laureate.json'

    def get(self) -> pd.DataFrame:
        r = requests.get(self.url)
        data = r.json()
        self.data = self.transform(data)
        return self.data

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        drop_cols = ['affiliations', 'share', 'overallMotivation']

        laureates = pd.DataFrame(data['laureates'])
        prizes = pd.io.json.json_normalize(
            data['laureates'],
            record_path='prizes',
            meta=['id'])

        prizes = prizes.drop(drop_cols, axis=1, errors='ignore')
        prizes.columns = prizes.columns.map(sid_to_id('nobel'))
        prizes = prizes.dropna(subset=['nobel_category'])
        laureates.columns = laureates.columns.map(sid_to_id('nobel'))
        laureates = laureates[laureates.columns.dropna()]

        df = prizes.merge(laureates, on='nobel_laureate')

        df.nobel_born_country = self._clean_country_col(df.nobel_born_country)
        df.nobel_died_country = self._clean_country_col(df.nobel_died_country)

        df['nobel_instance'] = df.nobel_category.str.cat(df.year, sep='_')
        df['nobel_prize'] = df.nobel_category.str.cat(
            [df.year, df.nobel_laureate], sep='_')

        df['year'] = df.year.astype(int)

        return df

    def _clean_country_col(self, series: pd.Series) -> pd.Series:
        return (series
                .str.replace(r'\([\w\' ]+\)', '')
                .str.replace('W&uuml;rttemberg', 'Württemberg')
                .str.replace('German-occupied Poland', 'Poland')
                .str.strip()
                .str.lower()
                .map(country_name_to_id))

    def save(self,
             path: Union[Path, str],
             recursive_concepts: bool = True,
             **kwargs: str) -> None:
        package = DataPackage(self.data)
        package.save(path, **kwargs)
