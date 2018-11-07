from obs.libs.s3 import login as login_lib
from obs.libs.utils import log_utils

def bucket_list(session=None):
    if not session:
        session = login_lib.get_client_session()

    bucket = session.list_buckets()
    try:
        list_bucket = bucket.__getitem__('Buckets')
        return list_bucket
    except Exception as e:
        log_utils.log_err(e)
        exit()


def put_bucket(session=None, name=None):
    if not session:
        session = login_lib.get_client_session()

    try:
        bucket = session.create_bucket(Bucket=name)
        return bucket.__getitem__('Location')
    except Exception as e:
        log_utils.log_err(e)
        exit()


def delete_bucket(session=None, name=None):
    if not session:
        session = login_lib.get_client_session()

    try:
        bucket = session.delete_bucket(Bucket=name)
        return bucket
    except Exception as e:
        log_utils.log_err(e)
        exit()
