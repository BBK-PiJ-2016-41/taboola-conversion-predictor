from conversion_predictor.CompoundFeatureCalculator import CompoundFeatureCalculator
import pandas as pd
from unittest import TestCase


class TaboolaConnectorTests(TestCase):

    def test_compound_feature_generator(self):
        test_data = pd.DataFrame({'ad_id': ['1'], 'cpc': [0.25], 'ctr': [0.10]})
        feature_calculator = CompoundFeatureCalculator(test_data)
        self.assertEqual(0.025, feature_calculator.calc_compound('cpc', 'ctr').iloc[0]['cpc_ctr'])

    def test_for_ad_id(self):
        with self.assertRaises(KeyError):
            CompoundFeatureCalculator(pd.DataFrame({'ad': ['1'], 'cpc': [0.25], 'ctr': [0.10]}))

    def test_for_bad_columns(self):
        test_data = pd.DataFrame({'ad_id': ['1'], 'cpc': [0.25], 'ctr': [0.10]})
        feature_calculator = CompoundFeatureCalculator(test_data)
        with self.assertRaises(KeyError):
            feature_calculator.calc_compound('cpx', 'ctx')
