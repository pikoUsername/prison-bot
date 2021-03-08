from discord import ClientUser
from discord.ext import commands


class Bot(commands.AutoShardedBot):
    __slots__ = 'on_startup_cbs', 'on_shutdown_cbs', 'welcome'

    def __init__(self, *args, welcome: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        self.on_startup_cbs = []
        self.on_shutdown_cbs = []

        self.welcome = welcome

    @property
    def me(self) -> ClientUser:
        if not hasattr(self, '_me'):
            setattr(self, '_me', self.user)
        return getattr(self, '_me')

    def on_startup(self, callback):
        if isinstance(callback, (list, tuple, set)):
            for cb in callback:
                self.on_startup_cbs.append(cb)

        assert callable(callback)
        self.on_startup_cbs.append(callback)

    def on_shutdown(self, callback):
        if isinstance(callback, (list, tuple, set)):
            for cb in callback:
                self.on_shutdown_cbs.append(cb)

        assert callable(callback)
        self.on_shutdown_cbs.append(callback)

    def _welcome(self):
        import logging

        log = logging.getLogger(__name__)
        user = self.me

        log.info(f"Welcome: {user.name if user else 'No User'}")
        log.info(f"Servers: {len(self.guilds)}")

    async def _shutdown(self):
        for callback in self.on_shutdown_cbs:
            await callback(self)
        await self.logout()

    async def _startup(self):
        for cb in self.on_startup_cbs:
            await cb(self)

    async def start(self, *args, **kwargs):
        if self.on_startup_cbs is not None: await self._startup()
        if self.welcome: self._welcome()
        await super().start(*args, **kwargs)
