from .requestors import S3Requestor
import requests, os, json
import botocore


class Bucket(object):
    def __init__(self, requestor):
        self.requestor = requestor

    def call(self, command, method=None):
        status_code = command['ResponseMetadata']['HTTPStatusCode']
        status_message = 'Command executed.'

        if method is None:
            data = command
        elif method == 'error':
            status_message = command['Error']['Message']
            data = []
        else:
            data = command[method]

        del command['ResponseMetadata']

        return {
            'status_code': status_code,
            'status_message': status_message,
            'data': data
        }

    def list_bucket(self):
        s3 = S3Requestor.request(self.requestor)

        try:
            return self.call(s3.list_buckets(), 'Buckets')
        except botocore.exceptions.ClientError as e:
            return self.call(e.response, 'error')

    def create_bucket(self, json=None):
        try:
            s3 = S3Requestor.request(self.requestor)

            url = s3.generate_presigned_url('create_bucket',
                                            Params={
                                                'Bucket': json['bucket'],
                                            },
                                            HttpMethod='PUT')

            headers = dict()
            if not json.get('policyid') is None:
                headers['x-gmt-policyid'] = json.get('policyid')

            if not json.get('acl') is None:
                headers['x-amz-acl'] = json.get('acl')

            if not json.get('grant_read') is None:
                headers['x-amz-grant-read'] = json.get('grant_read')

            if not json.get('grant_write') is None:
                headers['x-amz-grant-write'] = json.get('grant_write')

            if not json.get('grant_read_acp') is None:
                headers['x-amz-grant-read-acp'] = json.get('grant_read_acp')

            if not json.get('grant_write_acp') is None:
                headers['x-amz-grant-write-acp'] = json.get('grant_write_acp')

            if not json.get('grant_full_control') is None:
                headers['x-amz-grant-full-control'] = json.get('grant_full_control')

            try:
                create_bucket = requests.put(url, headers=headers)
                return {
                    'status_code': create_bucket.status_code,
                    'status_message': create_bucket.reason,
                    'data': create_bucket.url
                }
            except requests.exceptions.RequestException as err:
                return {
                    'status_code': 400,
                    'status_message': str(err),
                    'data': []
                }

        except KeyError as e:
            return {
                'status_code': 400,
                'status_message': 'Required parameter ' + str(e) + ' is missing.',
                'data': []
            }

    def delete_bucket(self, json=None):
        s3 = S3Requestor.request(self.requestor)

        try:
            return self.call(s3.delete_bucket(Bucket=json['bucket']))
        except KeyError as e:
            return {
                'status_code': 400,
                'status_message': 'Required parameter ' + str(e) + ' is missing.',
                'data': []
            }
        except botocore.exceptions.ClientError as e:
            return self.call(e.response, 'error')
