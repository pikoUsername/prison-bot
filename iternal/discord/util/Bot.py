import logging
from _contextvars import ContextVar

from discord import ClientUser, Message
from discord.ext import commands

from .middleware import MiddlewareManager
from .mixins import DataMixin

from .other import ctx_data, current_message
from .exceptions import CancelHandler
from .context import CtxContext


class Bot(commands.AutoShardedBot, DataMixin):
    """
    Bot with on_startup, on_shutdown
    and middleware
    """
    ctx_token = ContextVar("ctx_token")

    __slots__ = '_on_startup_cbs', '_on_shutdown_cbs', 'welcome', 'middleware'

    def __init__(self, *args, welcome: bool = 0x1, **kwargs):
        super().__init__(*args, **kwargs)

        self._on_startup_cbs = []
        self._on_shutdown_cbs = []
        self.welcome = welcome
        self.middleware = MiddlewareManager(self)

    @property
    def me(self) -> ClientUser:
        if not hasattr(self, '_me'):
            setattr(self, '_me', self.user)
        return getattr(self, '_me')

    async def process_commands(self, message: Message):
        data = {}
        ctx_data.set(data)

        # before
        try:
            # if pre_process_message chanes something
            # data changes too, dict is mutable, yay
            await self.middleware.trigger("pre_process_message", message, data)
        except CancelHandler:
            return

        try:
            ctx_token = current_message.set(message)
            try:
                # here processes message
                await self.middleware.trigger("process_message", message, data)
                await super().process_commands(message)
            finally:
                current_message.reset(ctx_token)
        except CancelHandler:
            pass
        finally:
            # after
            await self.middleware.trigger("post_process_message", message, data)

    async def get_context(self, message: Message, *, cls=CtxContext):
        ctx: CtxContext = await super().get_context(message, cls=CtxContext)
        ctx._data = ctx_data.get(None)
        return ctx

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
        if self._on_shutdown_cbs:
            for cb in self._on_shutdown_cbs:
                await cb(self)

        await self.logout()

    async def _startup(self):
        if self._on_shutdown_cbs:
            [await cb(self) for cb in self._on_startup_cbs]

    async def start(self, *args, **kwargs):
        await self._startup()
        if self.welcome: self._welcome()
        self.ctx_token.set(args[0])
        await super().start(*args, **kwargs)

    async def __aenter__(self):
        await self.start(self.ctx_token)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._shutdown()
