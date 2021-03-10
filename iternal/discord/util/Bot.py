import logging
from _contextvars import ContextVar

from discord import ClientUser, Message
from discord.ext import commands

from .middleware import MiddlewareManager
from .mixins import DataMixin


class Bot(commands.AutoShardedBot, DataMixin):
    """
    Bot with on_startup, on_shutdown
    and middleware
    """
    ctx_token = ContextVar("ctx_token")

    __slots__ = '_on_startup_cbs', '_on_shutdown_cbs', 'welcome', 'middleware_manager'

    def __init__(self, *args, welcome: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        self._on_startup_cbs = []
        self._on_shutdown_cbs = []
        self.welcome = welcome
        self.middleware_manager = MiddlewareManager(self)

    @property
    def me(self) -> ClientUser:
        if not hasattr(self, '_me'):
            setattr(self, '_me', self.user)
        return getattr(self, '_me')

    async def process_commands(self, message: Message):
        await self.middleware_manager.trigger("pre_process_message", message)
        await super().process_commands(message)
        await self.middleware_manager.trigger("post_process_message", message)

    def on_startup(self, callback):
        append = self._on_startup_cbs.append
        if isinstance(callback, (list, tuple, set)):
            [append(cb) for cb in callback]

        append(callback)

    def on_shutdown(self, callback):
        append = self._on_shutdown_cbs.append
        if isinstance(callback, (list, tuple, set)):
            [append(cb) for cb in callback]

        append(callback)

    def _welcome(self):
        user = self.me
        log = logging.getLogger(__name__)

        log.info(f"Welcome: {user.name if user else 'No User'}")
        log.info(f"Servers: {len(self.guilds)}")

    async def _shutdown(self):
        if self._on_shutdown_cbs is not None:
            for cb in self._on_shutdown_cbs:
                await cb(self)

        await self.logout()

    async def _startup(self):
        if self._on_shutdown_cbs is not None:
            [await cb(self) for cb in self._on_startup_cbs]

    async def start(self, *args, **kwargs):
        await self._startup()
        if self.welcome: self._welcome()
        await super().start(*args, **kwargs)

    async def __aenter__(self):
        await self.start(self.ctx_token)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._shutdown()
