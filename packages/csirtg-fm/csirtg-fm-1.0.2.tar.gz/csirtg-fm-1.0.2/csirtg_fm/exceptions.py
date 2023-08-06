
class CsirtgException(Exception):
    def __init__(self, msg):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg


class RuleUnsupported(CsirtgException):
    pass
