from pathlib import Path

import pytoml


class Config:
    def __init__(
        self,
        fp: Path,
        lazy: bool = True,
        setup_items: bool = False,
        **defaults
    ) -> None:
        self.fp = fp
        self.defaults = defaults
        self._cache = dict()

        if not lazy:
            self.load(cache=True)

        self.setup_items = setup_items

        if setup_items and not lazy:
            for k, v in self._cache.items():
                setattr(self, k, v)

    def load(self, cache: bool = 0x0):
        file = open(self.fp)
        try:
            data = pytoml.load(file)
            if data is None and self.defaults:
                data = self.defaults
        finally:
            file.close()

        if cache:
            self._cache = data

        return data

    def copy(self):
        if self._cache and not self.defaults:
            return self._cache.copy()

        if self.setup_items:
            return self

    def create_dsn(self):
        db = self._cache['db']
        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            db['user'], db['password'], db['host'], db['port'], db['database'])

        return url

    def __getitem__(self, key):
        if self._cache:
            return self._cache[key]

        if self.defaults:
            return self.defaults[key]

    __setitem__ = __delitem__ = lambda *_: None


config = Config(Path(__file__).parent / "configs" / "data.toml", lazy=False)
