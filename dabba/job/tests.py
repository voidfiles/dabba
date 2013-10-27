from dabba import Job
import unittest

class TestJob(unittest.TestCase):

    def test_job(self):
        data = {}

        self.assertRaises(Exception, Job.from_data, data)

        data['kind'] = 'awesome'

        self.assertRaises(Exception, Job.from_data, data)

        data['unique_id'] = 1

        job = Job.from_data(data)

        self.assertIsNotNone(job.get('id'))