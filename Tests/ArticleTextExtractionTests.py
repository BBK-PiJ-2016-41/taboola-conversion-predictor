from conversion_predictor.ArticleTextExtraction import UrlTransformer
import unittest
from unittest import TestCase
import pandas as pd

class UrlTester(TestCase):
    #
    def test_contains_ad_id(self):
        url_to_test = pd.DataFrame({'ad': ['1'], 'url': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        with self.assertRaises(KeyError):
            UrlTransformer(url_to_test)

    def test_contains_url(self):
        url_to_test = pd.DataFrame({'ad_id': ['1'], 'urloops': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        with self.assertRaises(KeyError):
            UrlTransformer(url_to_test)

    def test_url_not_text(self):
        url_to_test = pd.DataFrame({'ad_id': ['1'], 'url': [2]})
        with self.assertRaises(ValueError):
            UrlTransformer(url_to_test)

    def test_html_produced(self):
        url_to_test = pd.DataFrame({'ad_id': ['1'], 'url': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        transformer = UrlTransformer(url_to_test)
        result = transformer.extract_html()
        self.assertTrue('<' in result.iloc[0]['html'])

    def test_url_extracted(self):
        url_to_test = pd.DataFrame({'ad_id': ['1'], 'url': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        transformer = UrlTransformer(url_to_test)
        result = transformer.extract_domains()
        self.assertEquals(1.0, result.iloc[0]['expertsinmoney'])
        self.assertTrue('ad_id' in result.columns.values)
