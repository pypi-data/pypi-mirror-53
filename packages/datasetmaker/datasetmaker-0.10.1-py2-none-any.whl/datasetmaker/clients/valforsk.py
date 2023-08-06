import io
from pathlib import Path
from typing import Union
import pandas as pd
from datasetmaker.models import Client
from datasetmaker.datapackage import DataPackage
from datasetmaker.onto.manager import _map
from datasetmaker.utils import get_remote_zip


class ValforskClient(Client):
    url = ('https://www.dropbox.com/sh/8hdmg83o0o78ovn/'
           'AABdmOuIgpiOs99IMrgUTsHra?dl=1')

    def get(self) -> dict:
        z = get_remote_zip(self.url)

        mama = pd.read_csv(io.BytesIO(z['trender/utfil_bw15_mama.csv']))
        polls = pd.read_csv(io.BytesIO(z['polls.csv']))
        polls = self._clean_polls(polls)
        mama = self._clean_mama(mama)

        self.data = {
            'mama': mama,
            'polls': polls
        }

        return self.data

    def _clean_mama(self, df: pd.DataFrame) -> pd.DataFrame:
        df.date_actual = pd.to_datetime(df.date_actual)
        return df

    def _clean_polls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe with raw polling data"""

        # Calculate date between start an end
        df.coll_per_start = pd.to_datetime(df.coll_per_start)
        df.coll_per_end = pd.to_datetime(df.coll_per_end)
        polls_length = df.coll_per_end - df.coll_per_start
        df['date'] = (df.coll_per_start + (polls_length / 2)).dt.date

        # Drop redundant columns
        df = df.drop(['coll_per_start', 'coll_per_end'], axis=1)

        # Melt party columns
        party_cols = ['m', 'l', 'c', 'kd', 's', 'v',
                      'mp', 'sd', 'fi', 'pp', 'oth', 'dk']
        df = df.melt(id_vars=['pollster', 'date', 'samplesize'],
                     value_vars=party_cols,
                     var_name='party',
                     value_name='valforsk_opinion_value')

        df = df.rename(columns={'samplesize': 'valforsk_samplesize'})
        df.pollster = df.pollster.str.lower()
        df.party = df.party.map(_map('party', ['abbr'], 'party'))

        return df

    def save(self,
             path: Union[Path, str],
             recursive_concepts: bool = True,
             **kwargs: str) -> None:
        package = DataPackage(self.data['polls'], recursive_concepts)
        package.set_datapoints(measures=['valforsk_samplesize'],
                               keys=['pollster', 'date'])
        package.set_datapoints(measures=['valforsk_opinion_value'],
                               keys=['pollster', 'date', 'party'])
        package.save(path, **kwargs)
