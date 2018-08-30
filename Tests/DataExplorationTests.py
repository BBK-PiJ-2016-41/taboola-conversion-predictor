from unittest import TestCase
import pandas as pd
from conversion_predictor.Visualisation import Visualisation
from conversion_predictor.DataExploration import DataExploration


class UrlTester(TestCase):

    def setUp(self):
        data = pd.read_csv('C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\TextFilesAndCsvs\\TestOutput.csv')
        data.set_index('ad_id', inplace=True)
        data.drop('headline_text', axis=1)
        data.drop('url', axis=1)
        data.drop('domain', axis=1)
        visualiser = Visualisation(data)
        self.data_explorer = DataExploration(visualiser)

    def test_explorer(self):
        self.data_explorer.cmdloop()
