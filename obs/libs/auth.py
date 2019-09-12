import os
import boto3

from obs.libs import config


def resource():
    """Take credential and create boto session

    :return: resource service client.
    """
    config.load_config_file()
    access_key = os.environ.get("OBS_USER_ACCESKEY")
    secret_key = os.environ.get("OBS_USER_SECRETKEY")
    endpoint = os.environ.get("OBS_USER_URL")
    endpoint_url = f"https://{endpoint}"

    sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = sess.resource("s3", endpoint_url=endpoint_url)

    return s3_resource
