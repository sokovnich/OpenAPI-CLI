import logging

import requests
import six

from openapi_cli.auth.abstract import (
    AbstractAuth, OpenApiAuthException, log_request_curl
)


logger = logging.getLogger()

input = six.moves.input


class Decs3O(AbstractAuth):
    def __init__(self, token, refresh_token_url, verify=True):
        self.id_token = token
        self.refresh_token_url = refresh_token_url
        self.verify = verify

    @property
    def kwargs(self):
        return {
            'token': self.id_token,
            'refresh_token_url': self.refresh_token_url,
            'verify': self.verify,
        }

    @classmethod
    def input_creds(cls):
        return dict(
            client_id=input('Client ID: '),
            client_secret=input('Client secret: '),
            access_token_url=input('Access token URL: '),
            id_token_url=input('ID token URL: '),
        )

    @classmethod
    def from_creds(
            cls, client_id, client_secret,
            access_token_url, id_token_url,
            verify=True
    ):
        token = cls.get_jwt_token(
            client_id=client_id,
            client_secret=client_secret,
            access_token_url=access_token_url,
            id_token_url=id_token_url,
            verify=verify,
        )
        return cls(
            token=token,
            refresh_token_url='{}/refresh'.format(id_token_url),
            verify=verify,
        )

    def set_auth_header(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.id_token)

    def handle_401(self, response, **kwargs):
        if response.status_code == 401:
            # consume content to reuse connection for the next request
            response.content
            response.raw.release_conn()
            response.close()

            _request = response.request.copy()
            self.refresh_jwt_token()
            self.set_auth_header(r=_request)

            _response = response.connection.send(_request, **kwargs)
            _response.history.append(response)
            _response.request = _request

            response = _response

        log_request_curl(request=response.request)

        return response

    @staticmethod
    def get_jwt_token(
            client_id, client_secret,
            access_token_url, id_token_url,
            verify=True
    ):
        session = requests.Session()
        session.verify = verify

        response = session.post(
            access_token_url,
            data={
                'client_secret': client_secret,
                'grant_type': 'client_credentials',
                'client_id': client_id,
            }
        )
        token = response.json()
        response = session.post(
            '{id_token_url}?scope=user:memberOf:{clientid}:{scope}'.format(
                id_token_url=id_token_url,
                clientid=client_id,
                scope=token['scope']+'offline_access',
            ),
            headers={'Authorization': 'token {}'.format(token['access_token'])},
            verify=verify,
        )
        if response.status_code != 200:
            raise OpenApiAuthException("Cannot get JWT")

        return response.text

    def refresh_jwt_token(self):
        response = requests.get(
            url=self.refresh_token_url,
            headers={'Authorization': 'bearer {}'.format(self.id_token)},
            verify=self.verify,
        )
        if response.status_code != 200:
            raise OpenApiAuthException("Cannot refresh JWT")

        self.id_token = response.text

    def __call__(self, r):
        self.set_auth_header(r=r)
        r.register_hook("response", self.handle_401)

        return r
