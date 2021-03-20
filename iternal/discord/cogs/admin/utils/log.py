# https://github.com/pikoUsername/my_template_aiogram/blob/template/app/handlers/admin/debug/logs.py
import os
from pathlib import Path
from contextlib import suppress
from typing import Iterator

from iternal.discord.loader import proj_root

__all__ = "Logs",


# noinspection PyMethodMayBeStatic
class Logs:
    __slots__ = "logs_path",

    def __init__(self, logs_path: Path = None):
        if logs_path is None:
            logs_path = proj_root / "logs"
        self.logs_path = logs_path

    def last_file(self, fp: Path = None):
        """
        Get last log from /logs/ folder

        :return:
        """
        fp = fp or self.logs_path
        logs_list = os.listdir(fp)
        full_list = [os.path.join(fp, i) for i in logs_list]
        time_sorted_list = sorted(full_list, key=os.path.getmtime)
        with suppress(IndexError):
            return fp / time_sorted_list[-1]

    async def read_log(self, fp: Path, filter_) -> Iterator[str]:
        """
        Reads Whole log,
        and filters not need things
        """
        # might blocks, IO
        # but aiofiles.open not working
        f = open(fp)

        def log_filter(x: str):
            return filter_.lower() in x.lower()

        try:
            lines = filter(log_filter, f.readlines())
        finally:
            f.close()
        return lines

    async def read_logs(self, last=True, filters=None):
        filters = filters if filters else "INFO"
        logs_path = self.logs_path
        if last is False:
            # saving filter result and it s incredible, not efficient way
            # this list can store 1000 lines, of logs or more, but who cares?
            result = []
            for file in logs_path.glob("*"):
                # blocking io, so be careful about it
                # and i m lazy about correcting it.
                log = await self.read_log(file, filters)
                result.append(log)
            return result

        log = await self.read_log(Path(self.last_file(logs_path)), filters)
        return log
