from ..util.Bot import Bot


def setup(bot: Bot):
    from .i18n import I18nMiddleware

    bot.middleware.setup(I18nMiddleware)
