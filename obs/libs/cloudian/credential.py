from obs.libs.cloudian import requestors
from obs.libs.cloudian import user

def get(data=None, json=None, method='GET'):
    credentials = requestors.request(
                        url=user.base_url + '/credentials',
                        data=data,
                        json=json,
                        method=method)

    return credentials

def list(data=None, json=None, method='GET'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials/list',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials

def create(data=None, json=None, method='PUT'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials

def update(data=None, json=None, method='POST'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials

def status(data=None, json=None, method='POST'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials/status',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials

def delete(data=None, json=None, method='DELETE'):
    user_credentials = requestors.request(
                            url=user.base_url + '/credentials',
                            data=data,
                            json=json,
                            method=method)

    return user_credentials