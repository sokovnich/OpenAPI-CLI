# OpenAPI-CLI

![Workflow status](https://github.com/sokovnich/OpenAPI-CLI/actions/workflows/main.yml/badge.svg?branch=master)

OpenAPI-CLI is a CLI-client for any OpenAPI2.0-compatible API.

Main features:
* Dynamic CLI generation.
* Spec/authorization cache.
* Pluggable authentication.
* Python 2.7/3.5 support.

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

Clear spec/authorization cache:
```bash
openapi-cli --invalidate-cache
```

## How to generate a CLI-client stub:

Using another tool like https://github.com/OpenAPITools

## How to implement custom authentication plugin:

```python
import openapi_cli.auth.abstract

class MyAuth(openapi_cli.auth.abstract.AbstractAuth):
    ...
```
