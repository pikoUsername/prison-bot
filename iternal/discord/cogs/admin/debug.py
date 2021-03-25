from discord.ext import commands
from discord import Embed

from .utils import log
from iternal.discord.loader import proj_root
from iternal.store.prison import Prison
from iternal.discord.loader import _


class Debugger(commands.Cog, name='pantry | Кладовка'):
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show_logs", help=_("shows last logs"))
    @commands.is_owner()
    async def show_logs(self, ctx, file: str = None):
        if not file:
            last_log_path = log.last_file()
            with open(proj_root / "logs" / last_log_path) as f:
                result = f.read()
            e = Embed(
                title=last_log_path.name,
                description=result
            )
            await ctx.send(embed=e)
            return
        e = Embed(
            title=file,
            description="".join(await log.read_log(
                proj_root / "logs" / file
            ))
        )
        await ctx.send(embed=e)

    @commands.group(name="i18n")
    @commands.has_permissions(administrator=True)
    async def change_guild_language(self, ctx, language: str):
        try:
            await Prison.change_lang(language, ctx.guild.id)
        except TypeError as ex:
            await ctx.send(embed=Embed(
                title=_("Выбран неправильный язык"), description=f"```{str(ex)}```"
            ))
            return
        else:
            await ctx.send(_("Успешно изменен язык на {language}").format(language))
