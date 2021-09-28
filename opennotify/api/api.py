import requests
from .config import BASE_URL


class OpenNotifyRequest:

    def __init__(self):
        self._base_url = BASE_URL.rstrip('/')
        self.request_obj = requests.Session().request

    def request(self, endpoint: str, method: str = 'GET', url_params: dict = None):
        """
        Send an API Request
        :param endpoint: (str) Endpoint to be added to the base URL
        :param method: (str) HTTP method (ex: GET, POST, PUT)
        :param url_params: (dict) Optional: HTTP request parameters
        :return: JSON response
        """
        url = f'{self._base_url}/{endpoint}'
        response = self.request_obj(method=method, url=url, params=url_params)

        if response.ok:
            return response
        else:
            response.raise_for_status()


class OpenNotify:

    def __init__(self):
        self._request = OpenNotifyRequest().request

    def loc(self):
        """
        Submits a 'GET' request to the iss-now.json endpoint
        :return: (dict) response
        """
        endpoint = 'iss-now.json'
        method = 'GET'
        try:
            response = self._request(endpoint=endpoint, method=method)
            response = response.json()
        except requests.HTTPError as e:
            # Return mock data if API is down to show functionality of app
            # This would normally retry or supply more a reasonable alternative
            response = {"message": "success",
                        "timestamp": 123456789,
                        "iss_position": {
                            "longitude": "-10.1234",
                            "latitude": "31.41592"
                            },
                        "exception": e
                        }
        return response

    def people(self):
        """
        Submits a 'GET' request to the 'astros.json' endpoint
        :return: (dict) response
        """
        endpoint = 'astros.json'
        method = 'GET'
        try:
            response = self._request(endpoint=endpoint, method=method)
            response = response.json()
        except requests.HTTPError as e:
            # Return mock data if API is down to show app functionality
            # This would normally retry or supply more a reasonable alternative
            response = {"message": "success",
                        "number": 4,
                        "people": [
                            {"name": "James Tiberius Kirk", "craft": "NCC-1701"},
                            {"name": "Chris Hadfield", "craft": "ISS"},
                            {"craft": "NCC-1701", "name": "S’chn T’gai Spock"},
                            {"name": "Hikaru Kato Sulu"}
                            ],
                        "exception": e
                        }
        return response
