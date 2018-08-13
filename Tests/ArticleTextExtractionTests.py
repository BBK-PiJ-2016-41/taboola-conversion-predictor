from conversion_predictor.ArticleTextExtraction import UrlTransformer
import unittest
from unittest import TestCase
import pandas as pd

class UrlTester(TestCase):
    #
    def test_contains_ad_id(self):
        headline_to_test = pd.DataFrame({'ad': ['1'], 'url': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        with self.assertRaises(KeyError):
            UrlTransformer(headline_to_test)

    def test_contains_url(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'urloops': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        with self.assertRaises(KeyError):
            UrlTransformer(headline_to_test)

    def test_headline_not_text(self):
        headline_to_test = pd.DataFrame({'ad_id': ['1'], 'url': [2]})
        with self.assertRaises(ValueError):
            UrlTransformer(headline_to_test)
