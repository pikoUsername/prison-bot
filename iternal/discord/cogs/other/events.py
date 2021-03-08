from discord.ext.commands import errors
from discord import Embed
from discord.ext import commands


class Events(commands.Cog, name="events | Евенты"):
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
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
            errors.ChannelNotFound,
        )

        if isinstance(error, ignore_errors):
            pass

        elif isinstance(error, args_errors):
            await ctx.send("``Argument Error``, missing something, but what i wont tell you that")

        elif isinstance(error, commands.NotOwner):
            await ctx.reply(embed=Embed(
                    title="Permission Error",
                    description=f"{ctx.command}, Only for officers"
                )
            )

        else:
            await ctx.reply(f"Shit, Shit, how you can do this? {error}\n")
            owner = await self.bot.fetch_user(self.bot.owner_id)
            text = f"we have problem, in {ctx.guild.id} prison, and this is a problem: {error}"
            await owner.send(text)
