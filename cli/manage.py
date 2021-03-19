import asyncio

import click


@click.group()
def cli():
    from iternal.utils import logger

    logger.setup()


@cli.command()
@click.option('--prefix', '-p', default=None, type=str, help="What are you looking for?")
def discord(prefix: str):
    from iternal.discord.loader import bot

    def starter(bote: type(bot)):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(bote.start())
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(bote.shutdown())

    if prefix is not None:
        bot.command_prefix = prefix

    starter(bot)
