from __future__ import annotations

from typing import List
import logging

from discord import Message

log = logging.getLogger(__name__)


class MiddlewareManager:
    __slots__ = "bot", "applications"

    def __init__(self, bot) -> None:
        self.bot = bot
        self.applications: List[BaseMiddleware]

    def setup(self, middleware: BaseMiddleware) -> BaseMiddleware:
        assert isinstance(middleware, BaseMiddleware)
        assert middleware.is_configured()
        self.applications.append(middleware)
        middleware.setup(self)
        log.debug("Setuping %s to middleware manager" % middleware)
        return middleware

    async def trigger(self, action: str, message: Message) -> None:
        for app in self.applications:
            await app.trigger(action, message)


class BaseMiddleware:
    __slots__ = "_configured", "manager"

    def __init__(self) -> None:
        self._configured = 0
        self.manager = None

    def is_configured(self) -> None:
        assert self._configured, TypeError("%s Not configured" % self.__class__.__name__)

    def setup(self, manager: MiddlewareManager) -> None:
        self.manager = manager
        self._configured = 1

    async def trigger(self, action: str, message: Message) -> None:
        handler_name = f"on_{action}"
        handler = getattr(self, handler_name, None)
        if not handler:
            return None
        await handler(message)

