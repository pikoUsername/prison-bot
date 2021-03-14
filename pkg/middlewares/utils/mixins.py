from typing import Any, TypeVar, Type
from _contextvars import ContextVar

T = TypeVar("T")


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


class ContextMixin:
    def __init_subclass__(cls, **kwargs):
        cls.__context_instance = ContextVar(f"context_instance_{cls.__name__}")
        return cls

    @classmethod
    def get_current(cls: Type[T], no_err: bool = True):
        if no_err:
            cls.__context_instance.get(None)
        cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T):
        assert isinstance(value, cls), f"{value!r} is not subclass of {cls.__name__!r}"
        cls.__context_instance.set(value)
