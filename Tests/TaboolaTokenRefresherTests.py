from conversion_predictor.TokenRefresher import TaboolaTokenRefresher
from unittest import TestCase
from conversion_predictor.Factory import TokenRefresherFactory


class TaboolaTokenRefresherTests(TestCase):

    def test_status_code(self):
        token_refresher = TaboolaTokenRefresher()
        result = token_refresher.refresh_tokens()
        self.assertEqual(200, result[0])

    def test_factory_pattern(self):
        advertiser = 'mvfglobal-network'
        factory = TokenRefresherFactory()
        refresher = factory.get_object('Taboola')
        self.assertEqual(advertiser, refresher.advertiser)