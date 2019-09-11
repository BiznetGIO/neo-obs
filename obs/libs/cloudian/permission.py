from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils


base_url = "permission"


def get_permission(data=None, json=None, method="GET"):
    permission = requestors.request(url=base_url, data=data, json=json, method=method)

    try:
        permission_data = permission["data"]
    except Exception:
        log_utils.log_err(permission["status_message"])
    else:
        return permission_data


def create_permission(data=None, json=None, method="POST"):
    permission = requestors.request(url=base_url, data=data, json=json, method=method)

    try:
        permission_data = permission["data"]
    except Exception:
        log_utils.log_err(permission["status_message"])
    else:
        return permission_data
