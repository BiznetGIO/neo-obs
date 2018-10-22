import boto3
import botocore
import sys
from obs.libs.utils import env_utils


def init():
    env_s3 = env_utils.get_env_values_s3()
    region = env_s3['region']
    endpoint = env_s3['endpoint']
    key = env_s3['key']
    secret = env_s3['secret']
    s3client = boto3.client('s3',
                            region_name=region,
                            endpoint_url=endpoint,
                            aws_access_key_id=key,
                            aws_secret_access_key=secret)

    return s3client

def request(method, params):
    client = init()
    try:
        run_fn = getattr(client, method)(**params)
        data = {}
        for i in run_fn:
            if i != 'ResponseMetadata' and i != 'Owner':
                data[i] = run_fn[i]

        return {
            'status_code': run_fn['ResponseMetadata']['HTTPStatusCode'],
            'status_message': "Function '{}' successfully executed.".format(method),
            'data': data
        }
    except Exception as e:
        if hasattr(e, 'response'):
            return {
                'status_code': e.response['ResponseMetadata']['HTTPStatusCode'],
                'status_message': e.response['Error']['Message'],
                'data': {}
            }
        else:
            return {
                'status_code': 400,
                'status_message': str(e),
                'data': {}
            }
