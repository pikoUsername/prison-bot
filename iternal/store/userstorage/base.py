import typing


class BaseStorage:
    __slots__ = ()

    async def wait_closed(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def set_data(self, **kwargs):
        raise NotImplementedError

    async def get_data(self, key, no_error=True):
        raise NotImplementedError

    async def update_data(self, **kwargs):
        raise NotImplementedError

    @classmethod
    def check_address(cls, *,
                      guild: typing.Union[str, int, None] = None,
                      user: typing.Union[str, int, None] = None
                      ) -> (typing.Union[str, int], typing.Union[str, int]):
        """
        In all storage's methods chat or user is always required.
        If one of them is not provided, you have to set missing value based on the provided one.
        This method performs the check described above.
        :param guild:
        :param user:
        :return:
        """
        if not guild and not user:
            raise ValueError('`user` or `chat` parameter is required but no one is provided!')

        if not user and guild :
            user = guild
        elif user and not guild:
            guild = user
        return guild, user
