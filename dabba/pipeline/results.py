import json

class JsonResponse(object):

    def __init__(self, result_key):
        self.result_key = result_key

    def format_job_for_response(self, job, final_output_key):
        job_info = {
            'id': job.id,
            'kind': job.kind,
        }

        # If there were errors encode them into meta
        if job.get('errors'):
            job_info['errors'] = job.errors

        meta = {
            'job': job_info,
        }

        data = job.output.get(final_output_key, '')

        return json.dumps({
            'meta': meta,
            'resp': data,
        })
