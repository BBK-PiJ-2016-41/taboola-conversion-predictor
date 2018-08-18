from conversion_predictor.TaboolaTokenRefresher import TaboolaTokenRefresher
from unittest import TestCase


class TaboolaTokenRefresherTests(TestCase):

    def test_status_code(self):
        token_refresher = TaboolaTokenRefresher(
            'mvfglobal-network', '83f4ef05181643f99c6c0b2bc745ebcc', '34b2a2d5fe7749328c9e22ece77ef621')
        result = token_refresher.refresh_tokens()
        self.assertEqual(200, result[0])
