from typing import Any


class DataMixin:
    @property
    def data(self) -> dict:
        data = getattr(self, '_data', None)
        if not data:
            data = {}
            setattr(self, '_data', data)
        return data

    def __getitem__(self, key) -> Any:
        return self.data[key]

    def __setitem__(self, key, value) -> None:
        self.data[key] = value

    def __delitem__(self, key) -> None:
        del self.data[key]
