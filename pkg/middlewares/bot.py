import logging
from contextvars import ContextVar

from discord import ClientUser, Message
from discord.ext import commands

from .middleware import MiddlewareManager
from .utils.mixins import DataMixin, ContextMixin
from .exceptions import CancelHandler
from .utils.context import DataContext
from .utils.other import ctx_data, current_message


class Bot(commands.AutoShardedBot, DataMixin, ContextMixin):
    """
    Bot with on_startup, on_shutdown
    and middleware

    * You Should to call _shutdown method for correct shutdown
    """
    # needs for ctx_token
    # if you wont get token from config
    ctx_token = ContextVar("ctx_token")

    __slots__ = (
        '_on_startup_cbs',
        '_on_shutdown_cbs',
        'welcome',
        'middleware',
        'storage',
    )

    def __init__(
        self,
        *args,
        storage=None,
        welcome=True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Optional storage, see userstorages/
        self.storage = storage

        self._on_startup_cbs = []
        self._on_shutdown_cbs = []

        self.welcome = welcome

        self.middleware = MiddlewareManager(self)

        # for get_current
        self.set_current(self)

    @property
    def me(self) -> ClientUser:
        if not hasattr(self, '_me'):
            setattr(self, '_me', self.user)
        return getattr(self, '_me')

    async def process_commands(self, message: Message):
        if message.author.bot:
            return

        data = {}
        ctx_data.set(data)

        # before
        try:
            # if pre_process_message chanes something
            # data changes too, dict is mutable, yay
            await self.middleware.trigger("pre_process_message", (message, data))
        except CancelHandler:
            return

        try:
            ctx_token = current_message.set(message)
            try:
                # here processes message
                await self.middleware.trigger("process_message", (message, data))
                await super().process_commands(message)
            finally:
                current_message.reset(ctx_token)
        except CancelHandler:
            return
        finally:
            # after
            await self.middleware.trigger("post_process_message", (message, data))

    async def get_context(self, message: Message, *, cls=DataContext):
        ctx = await super().get_context(message, cls=DataContext)
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

    async def shutdown(self) -> None:
        if self._on_shutdown_cbs:
            for cb in self._on_shutdown_cbs:
                await cb(self)

        await self.logout()

    async def _startup(self) -> None:
        if self._on_shutdown_cbs:
            [await cb(self) for cb in self._on_startup_cbs]

    async def start(self, *args, **kwargs) -> None:
        """
        First starts startup callbacks

        :param args:
        :param kwargs:
        :return:
        """
        await self._startup()
        if self.welcome:
            self._welcome()
        self.ctx_token.set(args[0])
        await super().start(*args, **kwargs)

    async def on_message(self, message: Message):
        try:
            await self.process_commands(message)
        except Exception as exc:
            self.dispatch("on_command_error", exc)
            raise

    async def __aenter__(self):
        await self.start(self.ctx_token)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()
