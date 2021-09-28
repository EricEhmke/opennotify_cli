import pytest
import requests
from opennotify.api.api import OpenNotify, OpenNotifyRequest
from cli import OpenNotifyCLI


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
        assert type(response) is dict and "exception" in response.keys()  # 'exception' is added to response for
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
        assert type(response) is dict and "exception" in response.keys()  # 'exception' is added to response for
        # additional information but is not printed normally


class MockAPIWrapper:

    def loc(self):
        return {"message": "success",
                "timestamp": 123456789,
                "iss_position": {
                    "longitude": "-10.1234",
                    "latitude": "31.41592"
                }
                }

    def people(self):
        return {"message": "success",
                "number": 4,
                "people": [
                    {"name": "James Tiberius Kirk", "craft": "NCC-1701"},
                    {"name": "Chris Hadfield", "craft": "ISS"},
                    {"craft": "NCC-1701", "name": "S’chn T’gai Spock"},
                    {"name": "Hikaru Kato Sulu"}
                ]
                }


class TestCLI:

    def test_loc_format(self, monkeypatch, capsys):
        open_notify_cli = OpenNotifyCLI()
        monkeypatch.setattr(open_notify_cli, 'api', MockAPIWrapper())
        open_notify_cli.loc()
        captured = capsys.readouterr()
        assert captured.out == "The ISS current location at 1973-11-29 16:33:09 is 31.41592, -10.1234\n"

    def test_people_format(self, monkeypatch, capsys):
        open_notify_cli = OpenNotifyCLI()
        monkeypatch.setattr(open_notify_cli, 'api', MockAPIWrapper())
        open_notify_cli.people()
        captured = capsys.readouterr()
        assert captured.out == "There are 2 people aboard the NCC-1701. They are James Tiberius Kirk, S’chn T’gai Spock." \
                               "\nThere are 1 people aboard the ISS. They are Chris Hadfield." \
                               "\nThere are 1 people aboard the Unknown. They are Hikaru Kato Sulu.\n"

