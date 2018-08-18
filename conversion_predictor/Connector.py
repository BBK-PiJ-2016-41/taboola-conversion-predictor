from abc import ABC, abstractmethod
import requests as r

class Connector(ABC):


    def __init__(self):
        pass

    @abstractmethod
    def set_start_date(self, date):
        pass

    @abstractmethod
    def set_end_date(self, date):
        pass

    @abstractmethod
    def get_campaign_ids(self, file):
        pass

    @abstractmethod
    def get_data(self):
        pass
        
    @abstractmethod
    def set_credentials(self, authenticator):
        pass

    @abstractmethod
    def set_address(self, address):
        pass

    @abstractmethod
    def generate_url(self, campaign_id):
        pass


class TaboolaConnector(Connector):

    def __init__(self):
        self.address = "https://backstage.taboola.com/backstage/api/1.0/mvfglobal-network/reports/top-campaign-content/dimensions/item_breakdown"
        self.auth = "Bearer CdAAAAAAAAAAEYHpAAAAAAAAGAEgACk6tFnBZAEAADooZTI5ODUxMWY3ODJjODZmMWQxOGUyODQ0YTMxMjA0ZThiZDAyMmQ1MkAC::56b9cb::b263aa"
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
            data.append(request.json())
            response = request.status_code
        return [response, data]

    def set_credentials(self, authenticator):
        self.auth = authenticator

    def set_address(self, address):
        self.address = address

    def generate_url(self, campaign_id):
        return f"{self.address}?start_date={self.start_date}&end_date={self.end_date}&campaign={campaign_id}"
