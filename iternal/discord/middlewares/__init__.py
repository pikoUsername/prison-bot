from pkg.middlewares.bot import Bot
from loguru import logger


def setup(bot: Bot):
    from .acl import Acl

    logger.info("Setuping Middlewares")
    bot.middleware.setup(Acl())

