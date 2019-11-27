import os
import boto3
from distutils.util import strtobool
from cloudianapi.client import CloudianAPIClient
from requests_aws4auth import AWS4Auth

from obs.libs import config


def get_endpoint(bucket=None):
    """generate endpoint.

    Use `http` if ssl False otherwise `https`
    Use `example.com` if bucket False otherwise `bucketname.example.com`
    """
    hostname = os.environ.get("OBS_USER_URL")
    ssl = strtobool(os.environ.get("OBS_USE_HTTPS"))
    protocol = f"http{ssl and 's' or ''}://"
    bucket_name = f"{bucket and bucket or ''}{bucket and '.' or ''}"
    endpoint = f"{protocol}{bucket_name}{hostname}"
    return endpoint


def resource():
    """Take credential and create boto session

    :return: resource service client.
    """
    config.load_config_file()
    access_key = os.environ.get("OBS_USER_ACCESS_KEY")
    secret_key = os.environ.get("OBS_USER_SECRET_KEY")
    endpoint = get_endpoint()

    sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = sess.resource("s3", endpoint_url=endpoint)

    return s3_resource


def plain_auth():
    """Sign S3 the auth manually"""
    config.load_config_file()
    access_key = os.environ.get("OBS_USER_ACCESS_KEY")
    secret_key = os.environ.get("OBS_USER_SECRET_KEY")

    # "eu-west-1" just fake region that we didn't use
    # it must be supplied otherwise key sign failed
    auth = AWS4Auth(access_key, secret_key, "eu-west-1", "s3")

    return auth


def admin_client():
    """:return: CloudianApiClient object"""
    config.load_config_file()
    user = os.environ.get("OBS_ADMIN_USERNAME")
    passwd = os.environ.get("OBS_ADMIN_PASSWORD")
    endpoint = os.environ.get("OBS_ADMIN_URL")
    endpoint_url = f"http://{endpoint}"
    port = os.environ.get("OBS_ADMIN_PORT")
    client = CloudianAPIClient(url=endpoint_url, user=user, key=passwd, port=port)
    return client
