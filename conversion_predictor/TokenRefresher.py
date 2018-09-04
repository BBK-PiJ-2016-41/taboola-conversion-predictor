import requests as r
from abc import ABC, abstractmethod


class TokenRefresher(ABC):
    """
    Abstract Base Class for Token Refreshers.
    """

    def __init__(self):
        pass

    @abstractmethod
    def refresh_tokens(self):
        """
        Refreshes the tokens and returns the required credentials.
        :return:
        """
        pass


class TaboolaTokenRefresher(TokenRefresher):
    """
    Taboola Token Refresher class. Implements methods from TokenRefresher ABC.
    """

    def __init__(self, advertiser='mvfglobal-network'):
        """
        Constructor for Taboola Token Refresher.
        """
        super().__init__()
        self.advertiser = advertiser
        self.client_id = ''
        self.client_secret = ''

    def refresh_tokens(self):
        """
        Refreshes the tokens for Taboola
        :return: an array containing the response code, and the data
        """
        self.get_client_credentials()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        request = r.post('https://backstage.taboola.com/backstage/oauth/token?client_id=' + self.client_id +
                         '&client_secret=' + self.client_secret +
                         '&grant_type=client_credentials', headers=headers)
        json = request.json()
        data = 'Bearer ' + json['access_token']
        response = request.status_code
        return [response, data]

    def get_client_credentials(self):
        """
        Gets the client credentials from the user in order to maintain data security.
        """
        self.client_id = input('Please enter your client ID for Taboola')
        self.client_secret = input('Please enter your client secret for Taboola')
