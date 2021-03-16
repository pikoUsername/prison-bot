import logging
import sys

from loguru import logger

from data import LOGS_BASE_PATH


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


# noinspection PyArgumentList
def setup(disable: list = None, format: str = None):
    disable = disable or list()

    logger.add(sys.stderr, format=format or "{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(LOGS_BASE_PATH + "/file_{time}.log")

    if disable:
        for d in disable:
            logger.disable(d)
    logger.disable("sqlalchemy")

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
