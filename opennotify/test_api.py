import pytest
import requests
from collections import namedtuple
from .api.api import OpenNotify, OpenNotifyRequest


class MockRequestObjSuccess:
    def __init__(self, **kwargs):
        self.ok = True

    def json(self):
        return {"message": "success",
                "timestamp": 123456789,
                "iss_position": {
                    "longitude": "-10.1234",
                    "latitude": "31.41592"
                    }
                }


class MockRequestObjFail:
    def __init__(self, **kwargs):
        self.ok = False

    def raise_for_status(self):
        raise requests.HTTPError


class TestRequest:

    def test_request_success(self, monkeypatch):
        """
        Tests functionality of OpenNotifyRequest's handling of a successful response
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        mock_request = MockRequestObjSuccess
        open_notify_request = OpenNotifyRequest()
        monkeypatch.setattr(open_notify_request, 'request_obj', mock_request)
        response = open_notify_request.request(endpoint='example.com')
        assert True, response

    def test_request_fail(self, monkeypatch):
        """
        Tests functionality of OpenNotifyRequests's handling of a failed response
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        mock_request = MockRequestObjFail
        open_notify_request = OpenNotifyRequest()
        monkeypatch.setattr(open_notify_request, 'request_obj', mock_request)
        with pytest.raises(requests.HTTPError):
            open_notify_request.request(endpoint='example.com')


class TestAPI:

    def test_loc_success(self, monkeypatch):
        """
        Tests the wrapper of the loc endpoint for correct handling of a successful request
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        def mock_request(**kwargs):
            return MockRequestObjSuccess()
        open_notify_api = OpenNotify()
        monkeypatch.setattr(open_notify_api, '_request', mock_request)
        response = open_notify_api.loc()
        assert type(response) is dict

    def test_loc_fail(self, monkeypatch):
        """
        Tests the wrapper of the loc endpoint for correct handling of a successful request
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        def request_failed(**kwargs):
            raise requests.HTTPError

        open_notify_api = OpenNotify()
        monkeypatch.setattr(open_notify_api, '_request', request_failed)
        response = open_notify_api.loc()
        assert type(response) is dict and "exception" in response.keys() # 'exception' is added to response for
        # additional information but is not printed normally

    def test_people_success(self, monkeypatch):
        """
        Tests the wrapper of the loc endpoint for correct handling of a successful request
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        def mock_request(**kwargs):
            return MockRequestObjSuccess()
        open_notify_api = OpenNotify()
        monkeypatch.setattr(open_notify_api, '_request', mock_request)
        response = open_notify_api.people()
        assert type(response) is dict
    #

    def test_people_fail(self, monkeypatch):
        """
        Tests the wrapper of the loc endpoint for correct handling of a successful request
        :param monkeypatch: pytest fixture
        :return: assertion
        """
        def request_failed(**kwargs):
            raise requests.HTTPError

        open_notify_api = OpenNotify()
        monkeypatch.setattr(open_notify_api, '_request', request_failed)
        response = open_notify_api.loc()
        assert type(response) is dict and "exception" in response.keys() # 'exception' is added to response for
        # additional information but is not printed normally


class TestCLI:

    def test_loc_format(self):
        pass

    def test_people_format(self):
        pass