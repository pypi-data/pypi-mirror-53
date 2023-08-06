# mypy: allow-untyped-defs

import unittest
from unittest.mock import patch, PropertyMock
import datasetmaker as dam
from datasetmaker.path import ROOT_DIR
import pandas as pd


class TestValforskClient(unittest.TestCase):
    def setUp(self):
        url_patcher = patch('datasetmaker.clients.valforsk.ValforskClient.url',
                            new_callable=PropertyMock)
        mock_url = url_patcher.start()
        mock_url.return_value = ROOT_DIR.parent / 'tests/mock/valforskdata.zip'
        self.addCleanup(url_patcher.stop)

        self.client = dam.create_client(source='valforsk')
        self.df = self.client.get()

    def test_unzips_and_loads_data(self):
        self.assertEqual(type(self.df), dict)
        self.assertEqual(type(self.df['polls']), pd.core.frame.DataFrame)

