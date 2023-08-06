import shutil
from pathlib import Path
from typing import Generator, Union, List

import pandas as pd
from ddf_utils import package
from ddf_utils.io import dump_json
from cerberus import Validator

from datasetmaker.exceptions import EntityNotFoundException
from datasetmaker.onto.schemas import schema_registry
from datasetmaker.onto.manager import (
    entity_exists,
    read_entity,
    read_concepts)


class DataPackage:
    """"
    Class for automatically creating data packages from data frames.
    """
    datapoints: List = []

    def __init__(self,
                 data: Union[pd.DataFrame, list, dict],
                 recursive_concepts: bool = True) -> None:
        self.recursive_concepts = recursive_concepts
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, list):
            self.data = pd.concat(data, sort=True)
        else:
            self.data = pd.concat(data.values(), sort=True)
        self.concepts = self._find_concepts_recursiely()
        # self.concepts = self.concepts.dropna(axis=1, how='all')

    def _find_concepts_recursiely(self) -> pd.DataFrame:
        """
        Look up all concepts in the data, as well as any concepts
        that canonical entities in data reference.
        """
        concepts = list()
        initial_concepts = read_concepts(*self.data.columns)
        if not self.recursive_concepts:
            return initial_concepts
        for concept in initial_concepts.concept:
            concepts.append(concept)
            schema = schema_registry.get(concept)
            if schema:
                concepts.extend(list(schema.keys()))
        return read_concepts(*set(concepts))

    def _identity_entities(self) -> dict:
        """
        Identify all entity domains and role domains in the data.
        """
        return (self.concepts
                .query('concept_type.isin(["entity_domain", "role"])')
                .filter(['concept', 'domain'])
                .assign(domain=lambda x: x.domain.fillna(x.concept))
                .to_dict(orient='records'))

    def _assert_entity_is_valid(self, df: pd.DataFrame, schema: dict) -> None:
        """
        Raises if df does not conform to schema.

        TODO: Cerberus does not know of np.nan. Do we get away with fillna('')?
        """
        v = Validator(schema)
        data = df.fillna('').to_dict(orient='records')
        if not all(v.validate(x) for x in data):
            raise ValueError(v.errors)

    def _create_entity_frames(self) -> Generator:
        """
        For each entity in the data, create a pandas dataframe.
        """
        entities = self._identity_entities()
        domains = {x['domain'] for x in entities}

        for domain in domains:
            schema = schema_registry.get(domain)
            try:
                props = list(schema.keys())
            except AttributeError:
                raise EntityNotFoundException(domain)
            if entity_exists(domain) and domain in self.data:
                frame = read_entity(domain)
                frame = frame[frame[domain].isin(self.data[domain])]
            elif entity_exists(domain) and domain not in self.data:
                frame = read_entity(domain)
            else:
                frame = (self.data[props]
                         .dropna(subset=[domain])
                         .drop_duplicates(subset=[domain]))
            for entity in entities:
                if entity['domain'] != domain:
                    continue
                if entity['concept'] not in self.data:
                    continue
                frame = frame.merge(self.data[[entity['concept']]],
                                    left_on=domain,
                                    right_on=entity['concept'])
                if entity['concept'] != domain:
                    frame = frame.drop(entity['concept'], axis=1)
                frame = frame.drop_duplicates()
                if 'name' in frame and frame[['name']].shape[1] > 1:
                    frame = frame.pipe(
                        self._find_correct_name_col, entity=domain)
            self._assert_entity_is_valid(frame, schema)
            yield domain, frame

    def _find_correct_name_col(self,
                               df: pd.DataFrame,
                               entity: str) -> pd.DataFrame:
        """
        When multiple entities in the same dataframe have names,
        find the correct name column for the entity.
        """
        df.columns = [
            c if c != 'name' else f'name__{i}' for i, c in enumerate(df.columns)]
        for col in df.columns:
            if not col.startswith('name__'):
                continue
            if df[entity].unique().shape == df[col].unique().shape:
                break
        df = df.rename(columns={col: 'name'})
        df = df.drop([x for x in df.columns if x.startswith('name__')], axis=1)
        return df

    def set_datapoints(self, measures: list, keys: list) -> None:
        self.datapoints.append((measures, keys))

    def save(self, path: Union[Path, str], **kwargs: str) -> None:
        """
        Save the data as a DDF data package.
        """
        files = dict()

        path = Path(path)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir()

        for name, frame in self._create_entity_frames():
            files[f'ddf--entities--{name}.csv'] = frame

        for measures, keys in self.datapoints:
            measures_str = '--'.join(measures)
            keys_str = '--'.join(keys)
            fname = f'ddf--datapoints--{measures_str}--by--{keys_str}.csv'
            frame = (self.data[measures + keys]
                     .drop_duplicates()
                     .dropna())
            files[fname] = frame

        for fname, frame in files.items():
            frame.to_csv(path / fname, index=False)

        self.concepts.to_csv(path / 'ddf--concepts.csv', index=False)
        self._ddfify(path, **kwargs)

    def _ddfify(self, path: Path, **kwargs: Union[str, list]) -> None:
        """
        Read the contents of a DDF package and create a datapackage.json file.
        """
        kwargs['status'] = kwargs.get('status', 'draft')
        kwargs['title'] = kwargs.get('title', kwargs.get('name', ''))
        kwargs['topics'] = kwargs.get('topics', [])
        kwargs['default_measure'] = kwargs.get('default_measure', '')
        kwargs['default_primary_key'] = '--'.join(
            sorted(kwargs.get('default_primary_key', [])))
        kwargs['author'] = kwargs.get('author', 'Datastory')
        meta = package.create_datapackage(path, **kwargs)
        dump_json(path / 'datapackage.json', meta)
