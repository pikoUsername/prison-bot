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
        """
        :param fp: file path to config
        :param lazy: lazy loading
        :param setup_items: setattr to this object
                            all properies from config
        :param defaults:
        """
        self.fp = fp
        self.defaults = defaults
        self._cache = {}

        if not lazy:
            self.load(cache=True)

        self.setup_items = setup_items

        if setup_items and not lazy:
            for k, v in self._cache.items():
                setattr(self, k, v)

    def load(self, cache: bool = False):
        """
        Loads to cache a config properties

        :param cache:
        :return:
        """
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
        """
        Copies _cache property if _cache is not None

        :return:
        """
        if self._cache and not self.defaults:
            return self._cache.copy()

        if self.setup_items:
            return self

    def create_dsn(self):
        """
        Creates DSN or URL to postgres
        using in on_startup function

        :return:
        """
        db = self._cache['db']
        return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"

    def __getitem__(self, key):
        """
        Get item from cached settings

        :param key:
        :return:
        """
        if self._cache:
            return self._cache[key]

        if self.defaults:
            return self.defaults[key]

    __setitem__ = __delitem__ = lambda *_: None


config = Config(Path(__file__).parent / "configs" / "data.toml", lazy=False)
