# https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/contrib/middlewares/i18n.py
import gettext
import os
import typing
from contextvars import ContextVar
from typing import Any, Dict, Tuple

from babel.support import LazyProxy

from ..middleware import BaseMiddleware


class I18nMiddleware(BaseMiddleware):
    """
    I18n middleware based on gettext util
    >>> i18n = I18nMiddleware(DOMAIN, LOCALES_DIR)
    >>> bot.middleware.setup(i18n)
    and then
    >>> _ = i18n.gettext
    or
    >>> _ = i18n = I18nMiddleware(DOMAIN_NAME, LOCALES_DIR)
    """

    ctx_locale = ContextVar('ctx_user_locale', default=None)

    def __init__(self, domain, path=None, default='en') -> None:
        """
        :param domain: domain
        :param path: path where located all *.mo files
        :param default: default locale name
        """
        super(I18nMiddleware, self).__init__()

        if path is None:
            path = os.path.join(os.getcwd(), 'locales')

        self.domain = domain
        self.path = path
        self.default = default

        self.locales = self.find_locales()

    def __call__(self, singular, plural=None, n=1, locale=None) -> str:
        return self.gettext(singular, plural, n, locale)

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        """
        Load all compiled locales from path
        :return: dict with locales
        """
        translations = {}

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(self.path, name, 'LC_MESSAGES', self.domain + '.mo')

            if os.path.exists(mo_path):
                with open(mo_path, 'rb') as fp:
                    translations[name] = gettext.GNUTranslations(fp)
            elif os.path.exists(mo_path[:-2] + 'po'):
                raise RuntimeError(f"Found locale '{name}' but this language is not compiled!")

        return translations

    def reload(self) -> None:
        """
        Hot reload locales
        """
        self.locales = self.find_locales()

    @property
    def available_locales(self) -> Tuple[str]:
        """
        list of loaded locales
        :return:
        """
        return tuple(self.locales.keys())

    def gettext(self, singular, plural=None, n=1, locale=None) -> str:
        """
        Get text
        :param singular:
        :param plural:
        :param n:
        :param locale:
        :return:
        """
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    def lazy_gettext(self, singular, plural=None, n=1, locale=None, enable_cache=False) -> LazyProxy:
        """
        Lazy get text
        :param singular:
        :param plural:
        :param n:
        :param locale:
        :param enable_cache:
        :return:
        """
        return LazyProxy(self.gettext, singular, plural, n, locale, enable_cache=enable_cache)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        """
        User locale getter
        You can override the method if you want to use different way of getting user language.
        :param action: event name
        :param args: event arguments
        :return: locale name
        """
        raise NotImplementedError

    async def trigger(self, action, *args) -> typing.Optional[bool]:
        """
        Event trigger
        :param action: event name
        :param args: event arguments
        :return:
        """
        if 'update' not in action \
                and 'error' not in action \
                and action.startswith('pre_process'):
            locale = await self.get_user_locale(action, args)
            self.ctx_locale.set(locale)
            return True
