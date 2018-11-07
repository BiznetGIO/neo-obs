import os
import boto3
import dill
from obs.libs.utils import log_utils

S3_ENDPOINT='http://s3-stage.biznetgio.net:80'

def check_session():
    return os.path.isfile("/tmp/s3_session.pkl")


def get_client_session():
    try:
        if check_session():
            sess = None
            with open('/tmp/s3_session.pkl', 'rb') as f:
                sess = dill.load(f)
            return sess.client('s3', endpoint_url=S3_ENDPOINT)
        else:
            log_utils.log_err("Loading Session Failed")
            log_utils.log_err("Please login first")
    except Exception as e:
        log_utils.log_err("Loading Session Failed")
        log_utils.log_err("Please login first")
        log_utils.log_err(e)


def generate_session(access_key, secret_key):
    session = boto3.Session(aws_access_key_id=access_key,
                     aws_secret_access_key=secret_key)

    dump_session(session)
    return session


def dump_session(sess):
    try:
        with open('/tmp/s3_session.pkl', 'wb') as f:
            dill.dump(sess, f)
    except Exception:
        log_utils.log_err("Dump session failed")
