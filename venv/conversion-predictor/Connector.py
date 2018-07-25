from abc import ABC, abstractmethod

class Connector(ABC):


    def __init__(self):
        TODO

    @abstractmethod
    def set_start_date(self, date):
        TODO

    @abstractmethod
    def set_end_date(self, date):
        TODO

    @abstractmethod
    def get_campaign_ids(self, file):
        TODO

    @abstractmethod
    def get_data(self):
        TODO
        
    @abstractmethod
    def get_credentials(self, authenticator):
        TODO


class TaboolaConnector(Connector):

    def __init__(self):
        TODO

    def set_start_date(self, date):
        TODO

    def set_end_date(self, date):
        TODO

    def get_campaign_ids(self, file):
        TODO

    def get_data(self):
        TODO

    def get_credentials(self, authenticator):
        TODO