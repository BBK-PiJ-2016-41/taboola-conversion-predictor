import requests as r


class TaboolaTokenRefresher:

    def __init__(self, advertiser, client_id, client_secret):
        """
        Constructor class for Taboola Token Refresher.
        """
        self.advertiser = advertiser
        self.client_id = client_id
        self.client_secret = client_secret

    def refresh_tokens(self):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': 'x',
            'password': 'x',
            'grant_type': 'password'
        }
        options = {
            'payload': payload
        }
        request = r.post('https://backstage.taboola.com/backstage/oauth/token?client_id=' + self.client_id +
                         '&client_secret=' + self.client_secret +
                         'username=x&password=x&grant_type=password')
        data = 'Bearer ' + request.text
        print(data)
        response = request.status_code
        return [response, data]
