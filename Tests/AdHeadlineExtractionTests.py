from conversion_predictor.AdHeadlineExtraction import AdExtractor
import unittest
from unittest import TestCase
import pandas as pd
import numpy as np

class HeadlineTester(TestCase):
    def test_count_params(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'headline_text': ["Over 55s in ${city:capitalized}$ Can Now Use This Free Equity Release Calculator"]})
        ad_extractor = AdExtractor(headline_to_test)
        self.assertEqual(1, ad_extractor.num_dynamic_params().iloc[0]['num_params'])

    def test_count_zero_params(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'headline_text': ["Over 55s in London Can Now Use This Free Equity Release Calculator"]})
        ad_extractor = AdExtractor(headline_to_test)
        self.assertEqual(0, ad_extractor.num_dynamic_params().iloc[0]['num_params'])

    def test_count_puncs(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'headline_text': ["Over 55s in London Can Now Use This Free Equity Release Calculator!"]})
        ad_extractor = AdExtractor(headline_to_test)
        self.assertEqual(1, ad_extractor.num_punc_marks().iloc[0]['num_puncs'])

    def test_count_zero_puncs(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'headline_text': ["Over 55s in London Can Now Use This Free Equity Release Calculator"]})
        ad_extractor = AdExtractor(headline_to_test)
        self.assertEqual(0, ad_extractor.num_punc_marks().iloc[0]['num_puncs'])

    def test_count_all(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'headline_text': ["Over 55s in London Can Now Use This Free Equity Release Calculator"]})
        ad_extractor = AdExtractor(headline_to_test)
        result = ad_extractor.run_all()
        self.assertEquals(0, result.iloc[0]['num_params'])
        self.assertEquals(0, result.iloc[0]['num_puncs'])

    def test_contains_ad_id(self):
        headline_to_test = pd.DataFrame({'ad': ['1'], 'headline_text': ["Over 55s in London Can Now Use This Free Equity Release Calculator"]})
        with self.assertRaises(KeyError):
            AdExtractor(headline_to_test)

if __name__ == '__main__':
    unittest.main()
