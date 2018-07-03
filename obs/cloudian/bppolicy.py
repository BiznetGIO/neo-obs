from .requestors import CloudianRequestor


class BucketPolicy(object):
    base_url = 'bppolicy'

    def __init__(self, requestor):
        self.requestor = requestor

    def listpolicy(self):
        pass

    def bucketsperpolicy(self):
        pass
