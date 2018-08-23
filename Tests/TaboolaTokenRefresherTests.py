from conversion_predictor.TaboolaTokenRefresher import TaboolaTokenRefresher
from unittest import TestCase


class TaboolaTokenRefresherTests(TestCase):

    def test_status_code(self):
        token_refresher = TaboolaTokenRefresher()
        result = token_refresher.refresh_tokens()
        self.assertEqual(200, result[0])
