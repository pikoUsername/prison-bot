import random

from discord.ext import commands

from pkg.middlewares.utils import ctx_data
from iternal.discord.loader import _
from iternal.store.user import User


class Prison(commands.Cog, name="prison | Тюрьма"):
    """Your home | Твой милый дом"""
    __slots__ = "bot", "sys_rand"

    def __init__(self, bot):
        self.bot = bot
        self.sys_rand = random.SystemRandom()

    @commands.command(help=_('"Не попаду я в тюрягу"\n\tСказал Ты...'))
    async def start(self, ctx: commands.Context):
        data: dict = ctx_data.get()

        lang = data['guild'].get('language')

        # it s bad code ;(
        # check out for ru
        if lang == "ru":
            from .utils.consts import REASONS_RU as reasons
        else:
            from .utils.consts import REASONS_EN as reasons

        random_reason = self.sys_rand.choice(reasons)
        text = _(
            "Вы пасажены на бутылку за: {random_reason}\n"
            "Теперь вам уже не так смешно\n"
            "Теперь ты в говне, и тебе уже не так смешно\n"
            "Твоя задачя сбежать с этой тюрьмы\n"
        ).format(random_reason=random_reason)
        await ctx.reply(text)
        await User.to_imprison(ctx.author.id)

    @commands.command(name="", help="")
    async def talk(self, ctx: commands.Context, with_: str):
        pass

    @commands.command(name="inventory", help=_("Инвентарь"))
    async def inventory(self, ctx: commands.Context):
        pass

    @commands.command(name="", help=_("Номер"))
    async def cd(self, ctx: commands.Context):
        pass
