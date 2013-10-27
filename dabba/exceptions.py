

class BaseDabbaException(Exception):
    @property
    def message(self):
        return self.args[0]


class ProcessingException(BaseDabbaException):
    def __init__(self, message, slug=None, info=None):
        super(ProcessingException, self).__init__(message)
        self.slug = slug
        self.info = info


    def to_dict(self):
        return {
            'message': self.message,
            'slug': self.slug,
            'info': self.info,
        }


class EarlyReturn(BaseDabbaException):
    def __init__(self, message, job):
        super(EarlyReturn, self).__init__(message)
        self.job = job


class BadRequest(BaseDabbaException):
    def __init__(self, message, status_code=500):
        super(BadRequest, self).__init__(message)
        self.status_code = status_code