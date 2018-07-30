import boto3


class S3Requestor(object):
    def __init__(self, region, endpoint, key, secret):
        self.region = region
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

    def request(self, json=None, type='client'):
        if type == 'client':
            s3client = boto3.client('s3',
                                    region_name=self.region,
                                    endpoint_url=self.endpoint,
                                    aws_access_key_id=self.key,
                                    aws_secret_access_key=self.secret)
        else:
            s3client = boto3.resource('s3',
                                      region_name=self.region,
                                      endpoint_url=self.endpoint,
                                      aws_access_key_id=self.key,
                                      aws_secret_access_key=self.secret)

        return s3client
