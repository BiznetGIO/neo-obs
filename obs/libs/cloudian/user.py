from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils


base_url = 'user'


def get_list(data=None, json=None, method='GET'):
    base_url_list = base_url+'/list'
    list_user = requestors.request(
                        url=base_url_list,
                        data=data,
                        json=json,
                        method=method)
    try:
        data_user = list_user['data']
    except Exception as e:
        log_utils.log_err(list_user['status_message'])
        return None
    else:
        return data_user


def detail(data=None, json=None, method='GET'):
    get_user = requestors.request(
                        url=base_url,
                        data=data,
                        json=json,
                        method=method)

    try:
        data_user = get_user['data']
    except Exception as e:
        log_utils.log_err(get_user['status_message'])
        return None
    else:
        return data_user


def create(data=None, json=None, method='PUT'):
    create_user = requestors.request(
                            url=base_url,
                            data=data,
                            json=json,
                            method=method)

    try:
        data_user = create_user['data']
    except Exception as e:
        log_utils.log_err(create_user['status_message'])
        return None
    else:
        return data_user


def update(data=None, json=None, method='POST'):
    update_user = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    try:
        data_user = update_user['data']
    except Exception as e:
        log_utils.log_err(update_user['status_message'])
        return None
    else:
        return data_user


def delete(data=None, json=None, method='DELETE'):
    delete_user = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    try:
        data_user = delete_user['data']
    except Exception as e:
        log_utils.log_err(delete_user['status_message'])
        return None
    else:
        return data_user



