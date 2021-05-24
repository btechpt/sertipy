class SertipyException(Exception):

    def __init__(self, http_status, msg, reason=None):
        self.http_status = http_status
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return f'http status: {self.http_status}, {self.msg}, reason: {self.reason}'
