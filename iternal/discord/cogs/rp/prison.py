import random

from discord.ext import commands

from pkg.middlewares.utils import ctx_data

# stub
_ = str

class Prison(commands.Cog, name="prison | Тюрьма"):
    """Your home | Твой милый дом"""
    __slots__ = "bot", "sys_rand"

    def __init__(self, bot):
        self.bot = bot
        self.sys_rand = random.SystemRandom()

    @commands.command()
    async def start(self, ctx):
        _("""
        "Не попаду я в тюрягу"
          Said You...
        """)
        from .utils.consts import REASONS_RU

        try:
            data = ctx_data.get()
        except LookupError:
            data = None

        random_reason = self.sys_rand.choice(REASONS_RU)
        text = _(
            "Вы пасажены на бутылку за: {random_reason}\n"
            "Теперь вам уже не так смешно\n"
            "Теперь ты в говне, и тебе уже не так смешно\n"
            "Твоя задачя сбежать с этой тюрьмы\n"
        ).format(random_reason=random_reason)
        await ctx.reply(text)
