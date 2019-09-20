import os
import boto3
from cloudianapi.client import CloudianAPIClient

from obs.libs import config


def resource():
    """Take credential and create boto session

    :return: resource service client.
    """
    config.load_config_file()
    access_key = os.environ.get("OBS_USER_ACCESS_KEY")
    secret_key = os.environ.get("OBS_USER_SECRET_KEY")
    endpoint = os.environ.get("OBS_USER_URL")
    endpoint_url = f"https://{endpoint}"

    sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = sess.resource("s3", endpoint_url=endpoint_url)

    return s3_resource


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
