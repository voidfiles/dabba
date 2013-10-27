import requests

from bunch import Bunch

from dabba.exceptions import ProcessingException
from dabba.modules import BaseModule


class AddKeyModule(BaseModule):

    def __init__(self, key=None, *args, **kwargs):
        super(AddKeyModule, self).__init__(self)
        self.key = key

    def process(self, job):
        job = super(AddKeyModule, self).process(job)
        job[self.key] = True
        return job


class RequestsModule(BaseModule):
    default_input_key = 'http_request'

    def __init__(self, *args, **kwargs):
        requests_kwargs = ('method', 'url', 'headers', 'files', 'data', 'params', 'auth', 'cookies')
        # Pass through kwargs as the defaults for all http requests
        self.request_kwargs = {key:kwargs.pop(key, None) for key in requests_kwargs}

        super(RequestsModule, self).__init__(*args, **kwargs)


    def get_kwargs(self, job):
        kwargs = job.get(self.name, job.get(self.default_input_key))
        self.request_kwargs.update(kwargs)
        return self.request_kwargs

    def serialize_response(self, resp):
        content_type = resp.headers.get('Content-Type', 'application/json')
        try:
            content = resp.json()
        except Exception:
            content_type = content_type if content_type else 'application/text'
            content = resp.text

        history = map(lambda x: dict(url=x.url, status_code=x.status_code), resp.history)

        return Bunch.fromDict({
            'content': content,
            'headers': resp.headers,
            'history': history, 
        })

    def process(self, job):
        job = super(RequestsModule, self).process(job)

        kwargs = self.get_kwargs(job)

        try:
            resp = requests.request(**kwargs)
            resp.raise_for_status()
        except requests.exceptions.HTTPError, e:
            raise ProcessingException('A Connection error occurred.', slug='http_error', info=self.serialize_response(e.response))
        except requests.exceptions.RequestException, e:
            raise ProcessingException('There was an ambiguous exception that occurred while handling your request.', slug='request_exception')
        except requests.exceptions.ConnectionError, e:
            raise ProcessingException('A Connection error occurred.', slug='connection_error')
        except requests.exceptions.URLRequired, e:
            raise ProcessingException('A valid URL is required to make a request.', slug='url_required')
        except requests.exceptions.TooManyRedirects, e:
            raise ProcessingException('Too many redirects', slug='too_many_redirects')

        job.output[self.name] = self.serialize_response(resp)

        return job
