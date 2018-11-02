from obs.libs.s3 import requestors
import requests, os, json
import botocore
import boto3
from obs.libs.s3 import login as login_lib
from obs.libs.utils import log_utils


def bucket_list(session=None):
    if not session:
        session = login_lib.get_client_session()

    bucket = session.list_buckets()
    try:
        list_bucket = bucket.__getitem__('Buckets')
        return bucket
    except Exception as e:
        log_utils.log_err(e)
        exit()


def post_bucket(session=None, name=None, json=None):
    if not session:
        session = login_lib.get_client_session()

    try:
        if json is None:
            bucket = session.create_bucket(Bucket=name)
        else:
            bucket = session.create_bucket(
                Bucket=name,
                **json
            )

        return bucket
        
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
