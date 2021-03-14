from pathlib import Path

from .config import config

__all__ = "config", "LOGS_BASE_PATH"

LOGS_BASE_PATH = str(Path(__file__).parent.parent / "logs")
