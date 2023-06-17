import abc
import logging

import requests
import six

input = six.moves.input


@six.add_metaclass(abc.ABCMeta)
class AbstractAuth(requests.auth.AuthBase):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def kwargs(self):
        pass

    @classmethod
    def from_creds_user_input(cls, verify=True):
        print('{} authentication required.'.format(cls.__name__))
        return cls.from_creds(verify=verify, **cls.input_creds())

    @abc.abstractmethod
    def from_creds(cls, **kwargs):
        return cls(**kwargs)

    @abc.abstractmethod
    def input_creds(cls):
        return {
            'kwarg1': input('Kwarg1: '),
            'kwarg2': input('Kwarg2: '),
        }

    @abc.abstractmethod
    def __call__(self, r):
        return r


def log_request_curl(request):
    curl = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    headers = " -H ".join('"{0}: {1}"'.format(k, v) for k, v in request.headers.items())
    logging.debug(curl.format(method=request.method, headers=headers, data=request.body or "", uri=request.url))
