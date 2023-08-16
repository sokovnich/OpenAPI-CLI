# OpenAPI-CLI

![Workflow status](https://github.com/sokovnich/OpenAPI-CLI/actions/workflows/main.yml/badge.svg?branch=master)

OpenAPI-CLI is a CLI-client for any OpenAPI2.0-compatible API.

Key features:
* Runtime CLI generation.
* Spec/authorization cache.
* Pluggable authentication.
* Python 2.7/3.5+ support.

## How to install:
```bash
python setup.py install
python setup.py install_bash_completion
```

## How to use a CLI-client:

Initial setup:
```bash
export OPENAPI_CLI_BASE_URL='https://api-base-url'
export OPENAPI_CLI_VERIFY='false|true'
export OPENAPI_CLI_SPEC_URLS='https://spec-url1;https://spec-url2;...'
export OPENAPI_CLI_AUTH_PLUGIN='openapi_cli.auth.Decs3O'

openapi-cli -h
```

Clear authorization cache:
```bash
openapi-cli mngmt --invalidate-auth-cache
```

Clear specification cache:
```bash
openapi-cli mngmt --invalidate-spec-cache
```

Clear all caches:
```bash
openapi-cli mngmt --invalidate-cache
```

Enable debug logging:
```bash
openapi-cli <arg1> <arg2> --debug
```

Enable color output:
```bash
pip install pygments

openapi-cli <arg1> <arg2> --color
```

## How to implement custom authentication plugin:

```python
import openapi_cli.auth.abstract

class MyAuth(openapi_cli.auth.abstract.AbstractAuth):
    ...
```

## How to generate a CLI-client stub:

Using another tool like https://github.com/OpenAPITools
