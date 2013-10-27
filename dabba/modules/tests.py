import json
import unittest

import httpretty

from dabba import modules, Job
from dabba.exceptions import ProcessingException

class TestModule(unittest.TestCase):

    def setUp(self):
        self.job = Job.from_data(dict(kind='module_test', unique_id='1'))

    def test_base_module(self):
        module = modules.BaseModule()
        result = module.process(self.job)
        self.assertEquals(result, self.job)

    def test_add_key(self):
        module = modules.AddKeyModule(key='foo')
        result = module.process(self.job)
        self.assertIsNotNone(result.get('foo'))



class TestRequestsModule(unittest.TestCase):

    def setUp(self):
        httpretty.enable()
        self.data = {
            'awesome': 1,
        }

        self.data_json = json.dumps(self.data)

        self.job = Job.from_data({
            'kind': 'http',
            'unique_id': '1',
            'request_module': {
                'url': 'http://example.com',
                'method': 'GET',
            },
            'output': {},
        })

        self.request_module = modules.RequestsModule(name='request_module')

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def register_http_call(self, method=httpretty.GET, url='http://example.com', status=200, content_type='application/json'):
        return httpretty.register_uri(
            method,
            url,
            body=self.data_json,
            content_type=content_type,
            status=status,
        )

    def test_http_request_success(self):
        self.register_http_call()

        job = self.request_module.process(job=self.job)

        self.assertEquals(job.output.request_module.content.awesome, 1)

    def test_http_request_500(self):
        self.register_http_call(status=500)

        try:
            job = self.request_module.process(job=self.job)
        except Exception, e:
            pass

        self.assertIsInstance(e, ProcessingException)
