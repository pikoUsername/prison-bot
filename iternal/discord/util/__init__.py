from .Bot import Bot

__all__ = "Bot",


def get_util(key: str):
    return globals()[key]
