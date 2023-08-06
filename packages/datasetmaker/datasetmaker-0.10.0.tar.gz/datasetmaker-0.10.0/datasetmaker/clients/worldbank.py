import json
from pathlib import Path
from typing import Union
import requests
import pandas as pd
from datasetmaker.models import Client
from datasetmaker.datapackage import DataPackage
from datasetmaker.onto.manager import (
    _map,
    id_to_sid,
    sid_to_id)


non_countries = [
    'ARB',
    'CSS',
    'CEB',
    'EAR',
    'EAS',
    'EAP',
    'TEA',
    'EMU',
    'ECS',
    'ECA',
    'TEC',
    'EUU',
    'FCS',
    'HPC',
    'IBD',
    'IBT',
    'IDB',
    'IDX',
    'IDA',
    'LTE',
    'LCN',
    'LAC',
    'TLA',
    'LDC',
    'LMY',
    'MEA',
    'MNA',
    'TMN',
    'MIC',
    'NAC',
    'OED',
    'OSS',
    'PSS',
    'PST',
    'PRE',
    'SST',
    'SAS',
    'TSA',
    'SSF',
    'SSA',
    'TSS',
    'WLD']


class WorldBank(Client):
    indicators = ['worldbank_sp.dyn.le00.in', 'worldbank_sp.dyn.tfrt.in']
    # periods = [2015, 2016, 2017]

    def _get_wbi(self, code: str, **kwargs: str) -> pd.DataFrame:
        """Get a World Bank indicator for all countries."""

        url = f'http://api.worldbank.org/v2/country/all/indicator/{code}'
        kwargs.update({'format': 'json', 'page': 1, 'mrv': 2})
        last_page = -1
        data: list = []

        while last_page != kwargs["page"]:
            resp = requests.get(url, kwargs)
            meta, page_data = resp.json()
            last_page = meta["pages"]
            kwargs["page"] = kwargs["page"] + 1
            if page_data is None:
                continue
            if last_page == 1:
                break
            data.extend(page_data)

        df = pd.DataFrame(data)

        # Expand all dict columns
        for col in df.columns.copy():
            try:
                expanded = pd.io.json.json_normalize(
                    df[col], record_prefix=True)
                expanded.columns = [f"{col}.{x}" for x in expanded.columns]
                df = pd.concat([df, expanded], axis=1)
                df = df.drop(col, axis=1)
            except AttributeError:
                continue

        return df

    def get(self) -> pd.DataFrame:
        data = []
        # if self.periods and len(self.periods) > 1:
        #     date = f'{self.periods[0]}:{self.periods[-1]}'
        # elif self.periods:
        #     date = self.periods[0]
        # else:
        #     date = None

        for ind in self.indicators:
            code = id_to_sid('worldbank')[ind]
            frame = self._get_wbi(code)
            if frame.empty:
                continue
            frame = frame.dropna(subset=['value'])
            data.append(frame)
        df = pd.concat(data, sort=True).reset_index(drop=True)
        df = df.drop(["decimal", "obs_status", "unit",
                      "country.id", "indicator.value"], axis=1)

        # Remove non-countries
        df = df[df.countryiso3code != '']
        df = df[~df.countryiso3code.isin(non_countries)]

        # TODO: Make issue out of this special case
        df = df[df['country.value'] != 'West Bank and Gaza']

        # Standardize country identifiers
        iso3_to_id = _map('country', ['iso3'], 'country')
        name_to_id = _map(
            'country', ['name', 'alt_name'], 'country')
        df["country"] = df.countryiso3code.str.lower().map(iso3_to_id)
        df["country"] = df.country.fillna(df["country.value"].map(name_to_id))
        df = df.drop(["country.value", "countryiso3code"], axis=1)
        df = df[df.country.notnull()]
        df = df.rename(columns={"indicator.id": "indicator", "date": "year"})

        # Standardize indicator identifiers
        df.indicator = df.indicator.map(sid_to_id('worldbank'))

        df = (df
              .pivot_table(index=['country', 'year'],
                           values='value',
                           columns='indicator')
              .reset_index())

        self.data = df
        return df

    def save(self,
             path: Union[Path, str],
             recursive_concepts: bool = True,
             **kwargs: str) -> None:
        package = DataPackage(self.data)

        for indicator in self.indicators:
            package.set_datapoints(
                measures=[indicator], keys=['country', 'year'])

        package.save(path, **kwargs)
