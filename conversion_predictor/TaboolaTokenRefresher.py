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
