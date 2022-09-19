from openapi_cli.auth import Decs3O


def test_decs3o(mocker):
    mocker.patch("openapi_cli.auth.Decs3O.get_jwt_token", return_value='some.jwt.token')
    kwargs = Decs3O.from_creds(
        **dict(
            client_id='client_id', client_secret='client_secret',
            access_token_url='access_token_url', id_token_url='id_token_url',
            verify=False
        )
    ).kwargs

    assert Decs3O(**kwargs).kwargs == kwargs == {'token': 'some.jwt.token'}
