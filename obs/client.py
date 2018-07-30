from .cloudian.user import User
from .cloudian.qos import Qos
from .cloudian.bppolicy import BucketPolicy

from .s3.bucket import Bucket

from .cloudian.requestors import CloudianRequestor
from .s3.requestors import S3Requestor


class CloudianClient(object):
    def __init__(self, url, port, user, password):
        self._url = url
        self._port = port
        self._user = user
        self._password = password

        self._requestor = CloudianRequestor(self._url,
                                            self._port,
                                            self._user,
                                            self._password)

        self.user = User(self._requestor)
        self.qos = Qos(self._requestor)
        self.bppolicy = BucketPolicy(self._requestor)


class S3Client(object):
    def __init__(self, region, endpoint, key, secret):
        self.region = region
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

        self._requestor = S3Requestor(self.region,
                                      self.endpoint,
                                      self.key,
                                      self.secret)

        self.bucket = Bucket(self._requestor)
