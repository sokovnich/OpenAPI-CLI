import requests

from openapi_cli.auth.abstract import AbstractAuth, input


class Decs3O(AbstractAuth):
    def __init__(self, token):
        self.token = token

    @property
    def kwargs(self):
        return {'token': self.token}

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
        return cls(token=token)

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)

        return r

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
                scope=''.join(token['scope']),
            ),
            headers={'Authorization': 'token {}'.format(token['access_token'])},
            verify=verify,
        )
        return response.text
