from abc import ABC, abstractmethod
import requests as r


class Connector(ABC):

    def __init__(self):
        """
        Constructor for the Connector class and subclasses.
        """
        pass

    @abstractmethod
    def set_start_date(self, date):
        """
        Sets the start date for the date range required for data collection.
        :param date: The start date
        :return:
        """
        pass

    @abstractmethod
    def set_end_date(self, date):
        """
        Sets the end date for the date range required for data collection.
        :param date: The end date
        :param date:
        :return:
        """
        pass

    @abstractmethod
    def get_campaign_ids(self, file):
        """
        Gets the campaign ids for campaigns required for data collection and stores in the class.
        :param file: The name of the file in which the campaign ids are stored.
        :return:
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        Gets the data based on the dates and campaign id specifications
        :return: The response code of the HTTP request and the required data.
        """
        pass
        
    @abstractmethod
    def set_credentials(self, authenticator):
        """
        Sets the credentials for accessing the ad platform API.
        :param authenticator: The access token required.
        :return:
        """
        pass

    @abstractmethod
    def set_address(self, address):
        """
        Sets the address of the ad platform API.
        :param address: The address required.
        :return:
        """
        pass

    @abstractmethod
    def generate_url(self, campaign_id):
        """
        A helper function for getting data that generates the URL to which a HTTP request is made.
        :param campaign_id: The campaign id
        :return: The combined URL
        """
        pass


class TaboolaConnector(Connector):

    def __init__(self):
        self.address = "https://backstage.taboola.com/backstage/api/1.0/mvfglobal-network/reports/top-campaign-content/dimensions/item_breakdown"
        self.auth = "x"
        self.campaigns = []
        self.start_date = ""
        self.end_date = ""

    def set_start_date(self, date):
        if len(date) != 10 or '-' not in date:
            raise ValueError('Please make sure your date is in the format YYYY-MM-DD')
        self.start_date = date

    def set_end_date(self, date):
        if len(date) != 10 or '-' not in date:
            raise ValueError('Please make sure your date is in the format YYYY-MM-DD')
        self.end_date = date

    def get_campaign_ids(self, file):
        datafile = open(file, "r")
        try:
            lines = datafile.readlines()
            for line in lines:
                self.campaigns.append(line)
        except IOError:
            raise
        finally:
            datafile.close()

    def get_data(self):
        if len(self.campaigns) == 0:
            raise ValueError('Please specify a file with campaign IDs using get_campaign_ids()')
        data = []
        response = 0
        header = {"Authorization": self.auth}
        for campaign_id in self.campaigns:
            print(f"Accessing data for campaign: {campaign_id}")
            url = self.generate_url(campaign_id)
            request = r.get(url, headers=header)
            print(request.text)
            print(request.status_code)
            data.append(request.json())
            response = request.status_code
        return [response, data]

    def set_credentials(self, authenticator):
        self.auth = authenticator

    def set_address(self, address):
        self.address = address

    def generate_url(self, campaign_id):
        return f"{self.address}?start_date={self.start_date}&end_date={self.end_date}&campaign={campaign_id}"
