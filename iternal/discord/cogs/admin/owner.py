from discord.ext import commands as commands

from iternal.store.prison import Prison as Prison
from iternal.discord.loader import _ as __


class Owner(commands.Cog, name="owner | Владелец"):
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot
        setattr(self, '__doc__', __("Досуг для оффицеров"))

    @commands.command(name="i18n_prison")
    @commands.is_owner()
    async def change_lang_for_guild(self, ctx: commands.Context, gid: int, lang: str):
        """
        Changes language for exact gid
        """
        try:
            await Prison.change_lang(lang, gid)
        except TypeError:
            await ctx.send("не правильный язык, выбран вами. Оффицер, вам доступно только два стула")
        else:
            await ctx.send("Выбр за вами, оффицер!")
