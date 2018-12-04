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
        return groups_data