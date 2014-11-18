from pythonlsf import lsf as api
import logging


__all__ = [
    'create_empty_request',
    'create_reply',
    'init',
    'submit_job',
]


LOG = logging.getLogger(__name__)


def create_empty_request():
    request = api.submit()
    request.options = 0
    request.options2 = 0
    request.options3 = 0

    return request


create_reply = api.submitReply


def init():
    init_code = api.lsb_init(None)
    if init_code > 0:
        raise RuntimeError('Failed lsb_init, errno = %d' % api.lsb_errno())


def submit_job(request, reply):
    try:
        job_id = api.lsb_submit(request, reply)
    except:
        LOG.exception('Failed to submit LSF job')
        raise

    if job_id > 0:
        LOG.debug('Successfully submitted LSF job: %s', job_id)
        return job_id

    else:
        LOG.error('Failed to submit LSF job, return value = (%s), err = "%s"',
                job_id, api.lsb_sysmsg())
        raise RuntimeError('Failed to submit LSF job')