from pkg.middlewares import MiddlewareBot

from .util import CustomHelp


class PrisonRpBot(MiddlewareBot):
    """
    inheritance from Middleware Bot

    What about MiddlwareBot, Middleware Bot triggers
    middlewares in process_commands function, all middlewares

    * Note config takes from __init__ not from configs
      bc config might be a testing, or production,
      and need to change config, so it s not so cool
    """
    __slots__ = "config",

    def __init__(self, config, *args, **kwargs):
        super(PrisonRpBot, self).__init__(*args, **kwargs)
        self.config = config
        self.help_command = CustomHelp()

    async def start(self, *args, **kwargs):
        """
        Setup all stuff

        like database, on_startup, and db closing
        cogs setup, and middlewares,
        middleares list: i18n and acl
        """
        from . import cogs, middlewares
        from ..store import db

        token = self.config['bot']['TOKEN']

        db.setup(self)
        cogs.setup(self)
        middlewares.setup(self)

        await super().start(token, *args, **kwargs)
