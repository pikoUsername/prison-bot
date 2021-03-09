class i18n:
    __slots__ = "fp",

    def __init__(self, fp):
        self.fp = fp

    def gettext(self, text: str, *args):
        pass
