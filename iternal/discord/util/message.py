_message = __import__("discord").Message


class DateMessage(_message):
    """
    Stores Message data

    ctx_data uses in handlers/commands for get data
    """
    ctx_data = {}

    def __getitem__(self, key):
        return self.ctx_data[key]

    def __setitem__(self, key, value):
        self.ctx_data[key] = value

    def __delitem__(self, key):
        del self.ctx_data[key]


# for no import out
del _message
