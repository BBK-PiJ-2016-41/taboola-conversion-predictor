from abc import ABC, abstractmethod

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

    def set_address(self, address):
        pass


class TaboolaConnector(Connector):

    def __init__(self):
        self.address = "https://backstage.taboola.com/backstage/api/1.0/mvfglobal-network/reports/top-campaign-content/dimensions/item_breakdown"
        self.auth = "Bearer CdAAAAAAAAAAEYHpAAAAAAAAGAEgACk6tFnBZAEAADooZTI5ODUxMWY3ODJjODZmMWQxOGUyODQ0YTMxMjA0ZThiZDAyMmQ1MkAC::56b9cb::b263aa"
        self.campaigns = []

    def set_start_date(self, date):
        TODO

    def set_end_date(self, date):
        TODO

    def get_campaign_ids(self, file):
        TODO

    def get_data(self):
        TODO

    def set_credentials(self, authenticator):
        self.auth = authenticator

    def set_address(self, address):
        self.address = address