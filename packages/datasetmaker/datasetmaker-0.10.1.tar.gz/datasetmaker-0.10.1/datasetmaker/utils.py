from typing import Iterable, List, Union
import io
import zipfile
import pandas as pd
import requests


def get_remote_zip(url: str) -> dict:
    """
    Download a zipfile and load the contents into memory.

    Parameters
    ----------
    url : str
        URL to resource.

    Returns
    -------
    dict
        Dictionary with data keyed by filename.
    """
    if str(url).startswith('http'):
        content = requests.get(url).content
    else:
        with open(url, 'rb') as f:
            content = f.read()
    z = zipfile.ZipFile(io.BytesIO(content))
    return {name: z.read(name) for name in z.namelist()}


def pluck(seq: Iterable, name: str) -> List[str]:
    """
    Extracts a list of property values from list of dicts

    Parameters
    ----------
    seq : sequence, sequence to pluck values from.
    name : str, key name to pluck.
    """
    return [x[name] for x in seq]


def flatten(seq: Iterable) -> list:
    """
    Perform shallow flattening operation (one level) of seq

    Parameters
    ----------
    items : sequence, the sequence to flatten.
    """
    out = []
    for item in seq:
        for subitem in item:
            out.append(subitem)
    return out


def stretch(df: pd.DataFrame,
            index_col: Union[str, int],
            value_col: Union[str, int],
            sep: str = ';') -> pd.DataFrame:
    """
    Take a dataframe column with delimited values,
    and split the values into new rows.

    Parameters
    ----------
    df, dataframe to perform to operation on.
    index_col: str, identifying column.
    value_col: str, column with delimited values.
    sep: str, delimiting character.

    Examples
    --------
    >>> df = pd.DataFrame([['A;B', 1], ['C;D', 2]])
    >>> df
        0	1
    0	A;B	1
    1	C;D	2

    >>> stretch(df, index_col=1, value_col=0)
        index	0
    0	0	A
    1	1	B
    2	0	C
    3	1	D
    """
    return (df
            .set_index(index_col)
            .dropna(subset=[value_col])
            .loc[:, [value_col]]
            .stack()
            .str.split(';', expand=True)
            .stack()
            .unstack(-2)
            .reset_index(-1, drop=True)
            .reset_index())


class SDMXHandler:
    """
    Requesting and transforming SDMX-json data.

    Parameters
    ----------
    dataset : str, dataset identifier
    loc : list, list of countries
    subject : list, list of subjects

    Examples
    --------

    >>> sdmx = SDMXHandler('CSPCUBE', ['AUS', 'AUT'], ['FDINDEX_T1G'])
    >>> sdmx.data
    [{'Value': 0.0,
    'Year': '1997',
    'Subject': 'FDINDEX_T1G',
    'Country': 'AUT',
    'Time Format': 'P1Y',
    'Unit': 'IDX',
    'Unit multiplier': '0'}]
    """

    # TODO: URL should not be hardcoded
    base_url = "https://stats.oecd.org/sdmx-json/data"

    def __init__(self, dataset: str,
                 loc: list = [],
                 subject: list = [],
                 **kwargs: str):
        loc = "+".join(loc)  # type: ignore
        subject = "+".join(subject)  # type: ignore
        filters = f"/{subject}.{loc}" if loc or subject else ''
        url = f"{self.base_url}/{dataset}{filters}/all"
        r = requests.get(url, params=kwargs)
        self.resp = r.json()

    def _map_dataset_key(self, key: str) -> dict:
        key = [int(x) for x in key.split(":")]  # type: ignore
        return {y["name"]: y["values"][x]["id"] for
                x, y in zip(key, self.dimensions)}

    def _map_attributes(self, attrs: list) -> dict:
        attrs = [x for x in attrs if x is not None]
        return {y["name"]: y["values"][x]["id"] for
                x, y in zip(attrs, self.attributes)}

    @property
    def periods(self) -> dict:
        return self.resp["structure"]["dimensions"]["observation"][0]

    @property
    def dimensions(self) -> list:
        return self.resp["structure"]["dimensions"]["series"]

    @property
    def attributes(self) -> list:
        return self.resp["structure"]["attributes"]["series"]

    @property
    def data(self) -> list:
        observations = []
        for key, unit in self.resp["dataSets"][0]["series"].items():
            dimensions = self._map_dataset_key(key)
            attributes = self._map_attributes(unit["attributes"])
            z = zip(self.periods["values"], unit["observations"].items())
            for period, (_, observation) in z:
                data = {"Value": observation[0]}
                data[self.periods["name"]] = period["id"]
                data.update(dimensions)
                data.update(attributes)
                observations.append(data)
        return observations
