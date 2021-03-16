from __future__ import annotations

import typing
from typing import List
import logging

from discord import Message

log = logging.getLogger(__name__)


class MiddlewareManager:
    __slots__ = "bot", "applications"

    def __init__(self, bot) -> None:
        self.bot = bot
        self.applications: List[BaseMiddleware] = []

    def setup(self, middleware: BaseMiddleware) -> BaseMiddleware:
        assert isinstance(middleware, BaseMiddleware)
        if middleware.is_configured():
            raise ValueError('That middleware is already used!')

        self.applications.append(middleware)
        middleware.setup(self)
        log.debug("Setuping %s to middleware manager" % middleware)

        return middleware

    async def trigger(self, action: str, args: typing.Iterable) -> None:
        for app in self.applications:
            await app.trigger(action, args)


class BaseMiddleware:
    __slots__ = "_configured", "manager"

    def __init__(self) -> None:
        self._configured = False
        self.manager = None

    def is_configured(self) -> bool:
        return self._configured

    def setup(self, manager: MiddlewareManager) -> None:
        self.manager = manager
        self._configured = True

    async def trigger(self, action: str, args) -> None:
        handler_name = f"on_{action}"
        handler = getattr(self, handler_name, None)
        if not handler:
            return None
        await handler(*args)
