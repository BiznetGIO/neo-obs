
from obs.libs.cloudian import requestors


base_url = 'qos/limits'
def get(data=None, json=None, method='GET'):
    qos_details = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    return qos_details

def update(data=None, json=None, method='POST'):
    qos_details = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    return qos_details

def delete(data=None, json=None, method='POST'):
    qos_details = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    return qos_details
