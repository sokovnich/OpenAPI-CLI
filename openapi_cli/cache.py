import errno
import os
import shelve


class Cache:
    auth = None
    spec = None

    def __init__(self):
        self._cache_path = os.path.join(os.path.expanduser('~'), '.cache/openapi-cli')
        self._cache_auth_path = os.path.join(self._cache_path, 'auth.cache')
        self._cache_spec_path = os.path.join(self._cache_path, 'spec.cache')

        self._mkdirs(path=self._cache_path)
        self.open()

    def open(self):
        self.auth = shelve.open(self._cache_auth_path)
        self.spec = shelve.open(self._cache_spec_path)

    def invalidate(self):
        self.auth.clear()
        self.spec.clear()

    def close(self):
        self.auth.close()
        self.spec.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def _mkdirs(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if errno.EEXIST != e.errno:
                raise
