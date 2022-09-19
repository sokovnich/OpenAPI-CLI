import sys

import pytest

from openapi_cli.parser import parse_args
from openapi_cli.tests.specs import TEST_SPEC_YAML


@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', 'get'],
    ['openapi-cli', 'mngmt', '--invalidate-cache'],
    ['openapi-cli', 'v2', 'get'],
    ['openapi-cli', 'v2', 'test', 'post', '--testId', '1'],
])
def test_parse_args(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    parse_args(TEST_SPEC_YAML['paths'])


@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', 'get', '--dry-run'],
    ['openapi-cli', 'mngmt', '--invalidate-cache', '--dry-run'],
])
def test_parse_args_dry_run(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    parse_args(TEST_SPEC_YAML['paths'])


@pytest.mark.skipif(sys.version_info < (3,), reason='')
@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', '--dry-run'],
])
def test_parse_args_dry_run_2(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    parse_args(TEST_SPEC_YAML['paths'])
