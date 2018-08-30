from unittest import TestCase
import pandas as pd
from conversion_predictor.Visualisation import Visualisation
from conversion_predictor.DataExploration import DataExploration


class UrlTester(TestCase):

    def setUp(self):
        data = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        data.set_index('ad_id', inplace=True)
        data = data.drop('headline', axis=1)
        data = data.drop('page_text', axis=1)
        data = data.drop('url', axis=1)
        #data.drop('domain', axis=1)
        data = data.apply(pd.to_numeric)
        data = data.fillna(data.mean())
        visualiser = Visualisation(data)
        self.data_explorer = DataExploration(visualiser)

    def test_explorer(self):
        self.data_explorer.cmdloop()
