# mypy: allow-untyped-defs

import shutil
import pathlib
import unittest
from datasetmaker.datapackage import DataPackage
import pandas as pd


class TestDatapackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = pathlib.Path('datapackage_test_dir')
        if cls.path.exists():
            shutil.rmtree(cls.path)
        cls.path.mkdir()

        package = DataPackage(pd.DataFrame({
            'country': ['swe', 'ita', None, None],
            'esv_allocation': [None, None, '123', '456'],
            'name': [None, None, 'One', 'Two'],
            'sipri_milexp_cap': [10, 20, None, None],
            'esv_budget': [None, None, 50, 60]
        }))

        package.set_datapoints(['esv_budget'], ['esv_allocation'])
        package.save(cls.path)

    def test_package_has_concepts(self):
        self.assertTrue(True)
        self.assertTrue((self.path / 'ddf--concepts.csv').exists())

    def test_package_has_datapackage_json(self):
        self.assertTrue((self.path / 'datapackage.json').exists())

    def test_package_has_country_entity(self):
        self.assertTrue(
            (self.path / 'ddf--entities--country.csv').exists())

    def test_package_has_datapoints(self):
        datapoints_path = 'ddf--datapoints--esv_budget--by--esv_allocation.csv'
        self.assertTrue((self.path / datapoints_path).exists())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path)
