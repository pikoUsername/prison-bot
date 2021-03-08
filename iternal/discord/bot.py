from .util import Bot

__all__ = "PrisonRpBot",


class PrisonRpBot(Bot):
    __slots__ = "config",

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config

    async def start(self, *args, **kwargs):
        from . import cogs

        token = self.config['bot']['TOKEN']
        cogs.setup(self)
        await super().start(token, *args, **kwargs)
