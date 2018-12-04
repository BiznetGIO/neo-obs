from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils


base_url = 'group'
def group_list(data=None, json=None, method='GET'):
    url = base_url + '/list'

    groups = requestors.request(
                    url=url,
                    data=data,
                    json=json,
                    method=method)

    try:
        groups_data = groups['data']
    except Exception:
        log_utils.log_err(groups['status_message'])
    else:
        return [group['groupId'] for group in list(groups_data)]

def user_type_list():
    user_type = ['User', 'Admin']
    return user_type

def active_status():
    return ['true', 'false']