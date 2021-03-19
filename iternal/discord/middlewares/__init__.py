from pkg.middlewares.bot import Bot
from loguru import logger


def setup(bot: Bot):
    from .acl import Acl
    from ..loader import i18n

    logger.info("Setuping Middlewares")
    bot.middleware.setup(Acl())
    bot.middleware.setup(i18n)
