from ..util.Bot import Bot


def setup(bot: Bot):
    from .acl import Acl

    bot.middleware.setup(Acl())

