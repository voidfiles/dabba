import jsondate as json

from flask import Response
from werkzeug.contrib.atom import AtomFeed

class BaseResponse(object):
    content_type = None
    def __init__(self, result_key):
        self.result_key = result_key

    def format_meta_for_response(self, job):
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

        return meta

    def format_job_for_response(self, job):
        return job.output.get(self.result_key, '')


    def error(self, request, job=None, error=None):
        resp = {}

        if job:
            resp['meta'] = self.format_meta_for_response(job)

        if error:
            resp['data'] = unicode(error)
        else:
            resp['data'] = 'There was an unknown error'

        return self.return_response(resp, status=500)

    def success(self, request, job):
        return self.return_response({
            'meta': self.format_meta_for_response(job),
            'data': self.format_job_for_response(job),
        })

    def return_response(self, resp, status=200, content_type=None):
        if not content_type:
            content_type = self.content_type

        return Response(json.dumps(resp), status=status, content_type=content_type)


class JSONResponse(BaseResponse):
    content_type = 'application/json'


class ATOMResponse(BaseResponse):
    content_type = 'application/atom+xml'


    def error(self, request, job=None, error=None):
        resp = {}

        if job:
            resp['meta'] = self.format_meta_for_response(job)

        if error:
            resp['data'] = unicode(error)
        else:
            resp['data'] = 'There was an unknown error'


        return Response(json.dumps(resp), status=500, content_type='application/json')


    def success(self, request, job):
        feed = AtomFeed(job.feed_title, feed_url=request.url, url=request.url_root)
        for item in self.format_job_for_response(job):
            feed.add(item.title, unicode(item.description),
                     content_type='html',
                     author='echonest',
                     url=item.permalink,
                     updated=item.date,
                     published=item.date)

        return feed.get_response()
