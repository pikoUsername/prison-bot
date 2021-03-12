from discord.ext.commands import Context

from .mixins import DataMixin


class CtxContext(Context, DataMixin):
    """
    For Context data, with uses DataMixin
    and made for args, for example, connections
    """
