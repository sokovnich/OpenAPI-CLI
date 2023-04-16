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
    parse_args([TEST_SPEC_YAML])


@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', 'get', '--debug'],
    ['openapi-cli', 'v2', 'get', '--debug'],
])
def test_parse_args_debug(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    parse_args([TEST_SPEC_YAML])


@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', 'get', '--dry-run'],
    ['openapi-cli', 'mngmt', '--invalidate-cache', '--dry-run'],
])
def test_parse_args_dry_run(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    parse_args([TEST_SPEC_YAML])


@pytest.mark.parametrize("sys_argv", [
    ['openapi-cli', 'get'],
    ['openapi-cli', 'post'],
])
def test_parse_args_get_path_no_chain(monkeypatch, sys_argv):
    monkeypatch.setattr('sys.argv', sys_argv)
    args = parse_args([TEST_SPEC_YAML])

    assert args.path == '/'


def test_parse_args_no_args(monkeypatch):
    monkeypatch.setattr('sys.argv', ['openapi-cli'])
    with pytest.raises(SystemExit) as e:
        parse_args([TEST_SPEC_YAML])

        assert e.value.code == 2
