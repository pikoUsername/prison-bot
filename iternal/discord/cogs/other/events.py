from discord import ext, Embed as Embed

from iternal.discord.loader import _ as __


commands = ext.commands  # alias


class Events(commands.Cog, name="events | Евенты"):
    __slots__ = "bot", "command_activated"

    def __init__(self, bot):
        self.bot = bot
        self.command_activated = 0

    async def send_to_owner(
        self,
        *args, **kwargs
    ):
        owner = await self.bot.fetch_user(self.bot.owner_id)
        return await owner.send(*args, **kwargs)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errors = commands.errors  # alias

        args_errors = (
            errors.BadUnionArgument,
            errors.MissingRequiredArgument,
            errors.BadArgument,
            errors.TooManyArguments
        )

        ignore_errors = (
            errors.RoleNotFound,
            errors.CommandNotFound,
            errors.CommandOnCooldown,
            errors.ChannelNotFound
        )

        if isinstance(error, ignore_errors):
            return
        elif isinstance(error, args_errors):
            await ctx.send(__("``Argument Error``, Проебался, что то пропустил в аргментах"))
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(embed=Embed(
                title=__("Доступ запрещен"),
                description=__("%s, Только Для Оффицеров" % ctx.command)
            ))
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, AssertionError):
                await ctx.reply(error)
            else:
                await ctx.reply(__("Ну что же, у нас проблемки. {error}").format(error=error))
        else:
            await ctx.reply(__("Как ты это Сделал это? %s\n" % error))
            text = __(
                "У нас проблема, в тюрьме: %s, и эта проблема: %s"
            % (ctx.guild.name, error))
            await self.send_to_owner(text)

    @commands.Cog.listener()
    async def on_command_complete(self, *_):
        self.command_activated += 1
