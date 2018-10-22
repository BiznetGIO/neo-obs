from obs.libs.s3 import requestors
import requests, os, json
import botocore


def create_bucket(json=None):
    try:
        s3 = requestors.init()

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
                'data': {}
            }

    except KeyError as e:
        return {
            'status_code': 400,
            'status_message': 'Required parameter {} is missing.'.format(str(e)),
            'data': {}
        }
