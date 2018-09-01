from obs.libs.cloudian import requestors


base_url = 'user'

def list(data=None, json=None, method='GET'):
    base_url_list = base_url+'/list'
    list_user = requestors.request(
                        url=base_url_list,
                        data=data,
                        json=json,
                        method=method)

    return list_user

def get(data=None, json=None, method='GET'):
    get_user = requestors.request(
                        url=base_url,
                        data=data,
                        json=json,
                        method=method)

    return get_user

def create(data=None, json=None, method='PUT'):
    create_user = requestors.request(
                            url=base_url,
                            data=data,
                            json=json,
                            method=method)

    return create_user

def update(data=None, json=None, method='POST'):
    update_user = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    return update_user

def delete(data=None, json=None, method='DELETE'):
    delete_user = requestors.request(
                                url=base_url,
                                data=data,
                                json=json,
                                method=method)

    return delete_user



