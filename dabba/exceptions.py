

class ProcessingException(Exception):
    def __init__(self, message, slug=None, info=None):
        super(ProcessingException, self).__init__(message)
        self.slug = slug
        self.info = info

    @property
    def message(self):
        return self.args[0]

    def to_dict(self):
        return {
            'message': self.message,
            'slug': self.slug,
            'info': self.info,
        }


class EarlyReturn(Exception):
    def __init__(self, message, job):
        super(EarlyReturn, self).__init__(message)
        self.job = job

    @property
    def message(self):
        return self.args[0]
