from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils


base_url = 'qos/limits'


def get(data=None, json=None, method='GET'):
    qos_details = requestors.request(
        url=base_url,
        data=data,
        json=json,
        method=method)

    try:
        qos_data = qos_details['data']
    except Exception as e:
        log_utils.log_err(qos_details['status_message'])
        return None
    else:
        return qos_data


def update(data=None, json=None, method='POST'):
    qos_details = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    try:
        qos_data = qos_details['data']
    except Exception as e:
        log_utils.log_err(qos_details['status_message'])
        return None
    else:
        return qos_data


def delete(data=None, json=None, method='DELETE'):
    qos_details = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    try:
        qos_data = qos_details['data']
    except Exception as e:
        log_utils.log_err(qos_details['status_message'])
        return None
    else:
        return qos_data
