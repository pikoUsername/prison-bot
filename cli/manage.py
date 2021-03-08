import asyncio

import click


@click.group()
def cli():
    from iternal.utils import logger

    logger.setup()


@cli.command()
@click.option('--prefix', '-p', default=None, type=str, help="What are you looking for?")
def discord(prefix: str):
    from iternal.discord import bot
    from data import config

    prefix = prefix or config['bot']['prefix']
    b = bot.PrisonRpBot(config, command_prefix=prefix)

    def starter(bote):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(bote.start())
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            loop.run_until_complete(bote._shutdown())

    starter(b)
