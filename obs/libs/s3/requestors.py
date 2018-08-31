import boto3
import botocore
import sys


class S3Requestor(object):
    def __init__(self, region, endpoint, key, secret):
        self.region = region
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

    def init_client(self):
        s3client = boto3.client('s3',
                                region_name=self.region,
                                endpoint_url=self.endpoint,
                                aws_access_key_id=self.key,
                                aws_secret_access_key=self.secret)

        return s3client

    def call_fn(self, method, params):
        client = self.init_client()

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
