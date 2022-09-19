import json
import os
import sys
import urllib3

import requests
import six

from openapi_cli.cache import Cache
from openapi_cli.parser import parse_args
from openapi_cli.utils import import_object

input = six.moves.input
urlparse = six.moves.urllib.parse

BASE_URL = os.getenv('OPENAPI_CLI_BASE_URL')
SPEC_URLS = os.getenv('OPENAPI_CLI_SPEC_URLS', '').split(';')
AUTH_PLUGIN = os.getenv('OPENAPI_CLI_AUTH_PLUGIN')
VERIFY = os.getenv('OPENAPI_CLI_VERIFY', 'True').lower() in ['true', '1', 't', 'y', 'yes']

SUCCESS_CODES = [200, 201]


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


assert BASE_URL, 'OPENAPI_CLI_BASE_URL env must be defined and contain root API endpoint'
assert SPEC_URLS != [''], 'OPENAPI_CLI_SPEC_URLS env must be defined and contain OpenAPI spec urls separated by a semicolon'


def main():
    session = requests.Session()
    session.verify = VERIFY

    AuthClass = import_object(path=AUTH_PLUGIN)

    with Cache() as cache:
        if cache.auth.get('kwargs'):
            session.auth = AuthClass(**cache.auth['kwargs'])
        else:
            session.auth = AuthClass.from_creds_user_input(verify=VERIFY)
            cache.auth['kwargs'] = session.auth.kwargs

        specs = []
        for spec_url in SPEC_URLS:
            specs.append(
                cache.spec.get(spec_url) or cache.spec.setdefault(
                    spec_url, session.get(spec_url).json()
                )
            )

        args = parse_args(specs=specs)
        if getattr(args, 'dry_run', False):
            sys.exit()
        elif getattr(args, 'invalidate_cache', False):
            print('OpenAPI-CLI cache was successfully invalidated')
            cache.invalidate()
            sys.exit()

        url = urlparse.urljoin(BASE_URL, args.path)

        response = session.request(method=args.method, url=url, params=vars(args.kwargs) if hasattr(args, 'kwargs') else None)

        if response.status_code in SUCCESS_CODES:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            sys.exit(
                'Server unexpectedly responds with code {}:'
                '\n{}'.format(
                    response.status_code,
                    response.text
                )
            )


if __name__ == '__main__':
    main()
