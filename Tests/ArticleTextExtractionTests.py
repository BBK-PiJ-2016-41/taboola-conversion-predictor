from conversion_predictor.ArticleTextExtraction import UrlTransformer
from conversion_predictor.ArticleTextExtraction import HtmlTransformer
import unittest
from unittest import TestCase
import pandas as pd


class UrlTester(TestCase):

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

class HtmlTester(TestCase):

    def setUp(self):
        url_to_test = pd.DataFrame({'ad_id': ['1'], 'url': ["http://insurance.expertsinmoney.com/private-medical-insurance-sweeping-uk"]})
        transformer = UrlTransformer(url_to_test)
        self.html_result = transformer.extract_html()
        self.html_transformer = HtmlTransformer(self.html_result.drop('index', axis=1))

    def test_num_words(self):
        result = self.html_transformer.extract_total_words()
        self.assertEqual(604, result.iloc[0]['num_words'])

    def test_words_para(self):
        result = self.html_transformer.extract_words_para()
        self.assertEqual(46.4615, result.iloc[0]['words_para'])

    def test_num_paras(self):
        result = self.html_transformer.extract_num_paras()
        self.assertEqual(13, result.iloc[0]['num_paras'])

    def test_words_sentence(self):
        result = self.html_transformer.extract_words_sentence()
        self.assertEqual(13.7273, result.iloc[0]['words_sentence'])

    def test_clickouts(self):
        result = self.html_transformer.extract_clickouts()
        self.assertEqual(32, result.iloc[0]['num_clickouts'])

    def test_syllables_word(self):
        result = self.html_transformer.extract_syllables_word()
        self.assertEqual(1.4735, result.iloc[0]['syllables_word'])

    def test_run_all(self):
        result = self.html_transformer.extract_all()
        self.assertEqual(46.4615, result.iloc[0]['words_para'])
        self.assertEqual(604, result.iloc[0]['num_words'])
        self.assertEqual(13, result.iloc[0]['num_paras'])
        self.assertEqual(13.7273, result.iloc[0]['words_sentence'])
        self.assertEqual(1.4735, result.iloc[0]['syllables_word'])
        self.assertEqual(32, result.iloc[0]['num_clickouts'])
