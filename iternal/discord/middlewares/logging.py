import time
import logging

from discord import Message

from pkg.middlewares.middleware import BaseMiddleware


class LoggingMiddleware(BaseMiddleware):
    __slots__ = "logger", "_ftime"

    def __init__(self, log_name=__name__):
        super().__init__()
        logger = logging.getLogger(log_name)
        if logger is None:
            from loguru import logger
            self.logger = logger
        else:
            self.logger = logger

    def timer(self, stime: float):
        ftime = getattr(self, "_ftime", None)
        if ftime is not None:
            return stime - ftime
        return -1

    async def on_pre_process_message(self, message: Message, data: dict):
        setattr(self, '_ftime', time.perf_counter())
        self.logger.info((f"Pre processing message, Author: {message.author.display_name}\n"
                          f"Id: {message.id}, GuildId: {message.guild.id}"))

    async def on_post_process_message(self, message: Message, data: dict):
        f = self.timer(time.perf_counter()) * 1000
        self.logger.info(f"Post process Message, completed Time: [{f}ms]")
