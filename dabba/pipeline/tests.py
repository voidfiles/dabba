import unittest

from dabba import Pipeline, modules, Job
from dabba.exceptions import ProcessingException, EarlyReturn


class FakePipeline(Pipeline):
    add_foo = modules.AddKeyModule(key='foo')
    add_bar = modules.AddKeyModule(key='bar')


class MoreFakePipeline(FakePipeline):
    add_waz = modules.AddKeyModule(key='waz')


class ControlledErrorModule(modules.BaseModule):
    def process(self, job):
        raise ProcessingException('A controlled exception', slug='controlled_exception')


class UnControlledErrorModule(modules.BaseModule):
    def process(self, job):
        raise Exception('Uncontrolled Error')


class ControledFailurePipeline(Pipeline):
    controlled_error = ControlledErrorModule()


class UncontrolledFailurePipeline(Pipeline):
    uncontrolled_error = UnControlledErrorModule()


class ControledFailureNotRequiredPipeline(Pipeline):
    controlled_error = ControlledErrorModule(required=False)


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.job = Job.from_data(dict(kind='pipeline_test', unique_id='1'))

    def test_pipeline(self):
        fake_pipeline = FakePipeline(job=self.job)
        self.assertEqual(len(fake_pipeline.modules), 2)

        job = fake_pipeline.process()

        self.assertIsNotNone(job.get('foo'))
        self.assertIsNotNone(job.get('bar'))

    def test_extended_pipeline(self):
        extended_pipeline = MoreFakePipeline(job=self.job)

        job = extended_pipeline.process()

        self.assertIsNotNone(job.get('foo'))
        self.assertIsNotNone(job.get('bar'))
        self.assertIsNotNone(job.get('waz'))

    def test_controlled_exception(self):
        controlled_error_pipeline = ControledFailurePipeline(job=self.job)

        try:
            controlled_error_pipeline.process()
        except Exception, e:
            pass

        self.assertIsInstance(e, EarlyReturn)

        self.assertTrue(hasattr(e, 'job'))

        self.assertTrue(hasattr(e.job, 'errors'))

        self.assertTrue(e.job.errors[0]['module_name'] == 'controlled_error')

    def test_uncontrolled_exception(self):
        uncontrolled_error_pipeline = UncontrolledFailurePipeline(job=self.job)

        try:
            uncontrolled_error_pipeline.process()
        except Exception, e:
            pass

        self.assertIsInstance(e, EarlyReturn)

        self.assertTrue(hasattr(e, 'job'))

        self.assertTrue(hasattr(e.job, 'errors'))

    def test_failure_unrequired_module(self):
        controlled_error_pipeline = ControledFailureNotRequiredPipeline(job=self.job)
        job = controlled_error_pipeline.process()
        self.assertTrue(hasattr(job, 'errors'))
