from discord.ext.commands import Context

from pkg.middlewares.utils.mixins import DataMixin


class DataContext(Context, DataMixin):
    """
    For Context data, with uses DataMixin
    and made for args, for example, connections
    """
