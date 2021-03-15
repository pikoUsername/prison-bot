from discord.ext import commands

from pkg.middlewares.utils import ctx_data


class Prison(commands.Cog, name="prison | Тюрьма"):
    """Your home | Твой милый дом"""
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """
        "How to Come to jail? Just get fuck up"
          Said You...
        """
        text = (
            ""
            "Теперь ты в говне, и тебе уже не так смешно",
            "Твоя задачя сбежать с этой тюрьмы"
        )
        await ctx.reply()
