class DataMixin:
    @property
    def data(self):
        data = getattr(self, '_data')
        if not data:
            data = {}
            setattr(self, '_data', data)
        return data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]
