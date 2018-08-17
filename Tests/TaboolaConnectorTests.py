from conversion_predictor.Connector import TaboolaConnector
from unittest import TestCase


class TaboolaConnectorTests(TestCase):

    def setUp(self):
        self.connector = TaboolaConnector()

    def test_set_address(self):
        address = "address"
        self.connector.set_address(address)
        self.assertEqual(address, self.connector.address)

    def test_set_creds(self):
        creds = "creds"
        self.connector.set_credentials(creds)
        self.assertEqual(creds, self.connector.auth)

    def test_set_start_date(self):
        start_date = "2018-01-01"
        self.connector.set_start_date(start_date)
        self.assertEqual(start_date, self.connector.start_date)

    def test_start_date_format(self):
        start_date = "20180101"
        with self.assertRaises(ValueError):
            self.connector.set_start_date(start_date)


    def test_set_end_date(self):
        end_date = "2018-01-03"
        self.connector.set_end_date(end_date)
        self.assertEqual(end_date, self.connector.end_date)

    def test_get_campaign_ids(self):
        self.connector.get_campaign_ids("C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\TextFilesAndCsvs\\CampaignIds")
        self.assertEqual('603254', self.connector.campaigns[0])

    def test_get_campaign_ids_bad_file(self):
        file = "badfile"
        with self.assertRaises(IOError):
            self.connector.get_campaign_ids(file)

    def test_get_data(self):
        self.connector.get_campaign_ids(
            "C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\TextFilesAndCsvs\\CampaignIds")
        result = self.connector.get_data()
        print(result[1])
        self.assertEqual(result[0], 200)
