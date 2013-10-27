"""
Job Tracker Bundle
"""
import time

from bunch import Bunch

def generate_job_id(job_unique_id):
    return '%s_%s' % (job_unique_id, time.time())


class Job(Bunch):

    @classmethod
    def from_data(cls, data):

        job = cls.fromDict(data)

        if not job.kind:
            raise Exception("A job must have a kind")

        if not job.unique_id:
            raise Exception('A job must have q unique_id')

        job.id = generate_job_id(job.unique_id)

        return job

    def __repr__(self):
        return "Job(id='%s', kind='%s')" % (self.id, self.kind)