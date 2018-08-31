from .requestors import CloudianRequestor


class BucketPolicy(object):
    base_url = 'bppolicy'

    def __init__(self, requestor):
        self.requestor = requestor

    def list(self, data=None, json=None, method='GET'):
        list_policy = CloudianRequestor.request(self.requestor,
                                                url=self.base_url + '/listpolicy',
                                                data=data,
                                                json=json,
                                                method=method)

        return list_policy

    def get(self, data=None, json=None, method='GET'):
        detail_policy = CloudianRequestor.request(self.requestor,
                                                  url=self.base_url,
                                                  data=data,
                                                  json=json,
                                                  method=method)

        return detail_policy

    def buckets(self, data=None, json=None, method='GET'):
        bucket_policy = CloudianRequestor.request(self.requestor,
                                                  url=self.base_url + '/bucketsperpolicy',
                                                  data=data,
                                                  json=json,
                                                  method=method)

        return bucket_policy
