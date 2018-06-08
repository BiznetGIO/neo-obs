class CloudianClient(object):
    def __init__(self, url, port, user, password):
        self._url = url
        self._port = port
        self._user = user
        self._password = password


class S3Client(object):
    def __init__(self, region, endpoint, key, secret):
        self.region = region
        self.endpoint = endpoint
        self.key = key
        self.secret = secret