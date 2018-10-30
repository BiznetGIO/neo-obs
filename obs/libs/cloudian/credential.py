from obs.libs.cloudian import requestors
from obs.libs.cloudian import user
from obs.libs.utils import log_utils


def get_credential(data=None, json=None, method='GET'):
    url = user.base_url
    if 'accessKey' in data:
        url = url + '/credentials'
    elif 'userId' in data and 'groupId' in data:
        url = url + '/credentials/list'
        if 'active' in data:
            url = url + '/active'

    credentials = requestors.request(
                        url=url,
                        data=data,
                        json=json,
                        method=method)

    try:
        credentials_data = credentials['data']
    except Exception:
        log_utils.log_err(credentials['status_message'])
    else:
        return credentials_data


def create(data=None, json=None, method='PUT'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials',
                            data=data,
                            json=json,
                            method=method)
    
    try:
        user_credentials_data = user_credentials['data']
    except Exception:
        log_utils.log_err(user_credentials['status_message'])
    else:
        return user_credentials_data

def update(data=None, json=None, method='POST'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials/status',
                            data=data,
                            json=json,
                            method=method)

    try:
        user_credentials_data = user_credentials['data']
    except Exception:
        log_utils.log_err(user_credentials['status_message'])
    else:
        return user_credentials_data

def delete(data=None, json=None, method='DELETE'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials