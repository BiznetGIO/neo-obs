from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils

base_url = 'usage'

def get_usage(data=None, json=None, method='GET'):
    usage = requestors.request(
                        url=base_url,
                        data=data,
                        json=json,
                        method=method)

    try:
        usage_data = usage['data']
    except Exception:
        log_utils.log_err(usage['status_message'])
    else:
        return usage_data