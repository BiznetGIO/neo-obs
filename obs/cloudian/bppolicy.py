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
