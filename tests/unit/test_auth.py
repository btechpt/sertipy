import json
import responses

from unittest import TestCase

from sertipy.exceptions import SertipyException
from sertipy.auth import SertivaAuth


class TestAuth(TestCase):
    def setUp(self):
        self.auth = SertivaAuth('', '')
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)


class TestInit(TestAuth):
    def test_initial_client_id(self):
        self.assertEqual(self.auth.client_id, '')

    def test_initial_client_secret(self):
        self.assertEqual(self.auth.client_secret, '')


class TestGetToken(TestAuth):
    def test_get_token(self):
        # given
        token = "ACCESS TOKEN"
        data = {"code": 200, "status": "success",
                "data": {
                    "token_type": "Bearer",
                    "expires_in": 31536000,
                    "access_token": token
                }}

        self.responses.add(
            responses.POST, 'https://api.sertiva.id/api/v2/authorization',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.auth.get_token()

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(token, resp)

    def test_get_token_exception(self):
        # given
        url = 'https://api.sertiva.id/api/v2/authorization'
        data = {
            "code": 400,
            "status": "fail",
            "message": "There was a problem with the data submitted"
        }

        self.responses.add(
            responses.POST, url,
            body=f'{json.dumps(data)}',
            status=400,
            content_type='application/json')

        # taken
        with self.assertRaises(SertipyException):
            # when
            self.auth.get_token()
