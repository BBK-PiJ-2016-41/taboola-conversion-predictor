from conversion_predictor.AdHeadlineExtraction import AdExtractor
import unittest
from unittest import TestCase
import pandas as pd

class HeadlineTester(TestCase):
    def test_count_params(self):
        headline_to_test = pd.DataFrame(columns=["ad_id, headline_text"], data=["1", "Over 55s in ${city:capitalized}$ Can Now Use This Free Equity Release Calculator"])
        ad_extractor = AdExtractor(headline_to_test)
        print(ad_extractor.num_dynamic_params())
        self.assertEquals(2, ad_extractor.num_dynamic_params())

if __name__ == '__main__':
    unittest.main()
