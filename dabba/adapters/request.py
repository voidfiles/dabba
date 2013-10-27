from functools import wraps

from dabba.exceptions import EarlyReturn, BadRequest

def flask_request_to_job(pipeline_class, response_adapter):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            try:
                job, request = f(*args, **kwds)
            except BadRequest, e:
                return (e.message, e.status_code)
            except:
                return ('Bad request', 500)

            pipeline = pipeline_class(job=job)
            try:
                job = pipeline.process()
            except EarlyReturn, e:
                return response_adapter.error(request, e.job, e)
            except:
                return response_adapter.error(request, )

            return response_adapter.success(request, job)

        return wrapper
    return decorator