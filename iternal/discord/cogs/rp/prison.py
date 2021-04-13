import random
from typing import Any

import asyncpg
from discord.ext import commands

from pkg.middlewares.utils import ctx_data
from iternal.discord.loader import _
from iternal.store.user import User


class ItemConvertor(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: Any) -> None:
        _data: dict = ctx_data.get()
        try:
            user: asyncpg.Record = _data['user']
        except KeyError:
            await ctx.send(_(
                "Ух, как вот так можно?\n"
                "Сломать то что не сломать\n"
            ))
            return
        inventory = user.get('inventories')
        # TODO: use ORM instead of sql


class Prison(commands.Cog, name="prison | Тюрьма"):
    """Your home | Твой милый дом"""
    __slots__ = "bot", "sys_rand"

    def __init__(self, bot):
        self.bot = bot
        self.sys_rand = random.SystemRandom()

    async def cog_check(self, ctx: commands.Context) -> bool:
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

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
    async def prisoner_inventory(self, ctx: commands.Context):
        pass

    @commands.command(name="card", aliases=["cd"], help=_("Номер"))
    async def prisoner_cd(self, ctx: commands.Context) -> None:
        pass

    @commands.command(name="go")
    async def prisoner_go(self, ctx: commands.Context) -> None:
        pass

    @commands.group(name="craft")
    async def prisoner_craft(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            _t = ctx.send_help(ctx.command)
            await _t

    @prisoner_craft.command(aliases=["item"], help=_("\0"))
    async def make_craft(self, ctx: commands.Context, item: ItemConvertor):
        pass
