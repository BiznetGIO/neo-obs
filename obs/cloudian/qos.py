from .requestors import CloudianRequestor


class Qos(object):
    base_url = 'qos/limits'

    def __init__(self, requestor):
        self.requestor = requestor

    def get(self, data=None, json=None, method='GET'):
        qos_details = CloudianRequestor.request(self.requestor,
                                                url=self.base_url,
                                                data=data,
                                                json=json,
                                                method=method)

        return qos_details

    def update(self, data=None, json=None, method='POST'):
        qos_details = CloudianRequestor.request(self.requestor,
                                                url=self.base_url,
                                                data=data,
                                                json=json,
                                                method=method)

        return qos_details
