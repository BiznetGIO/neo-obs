from obs.libs.cloudian import requestors
from obs.libs.utils import log_utils


base_url = "bppolicy"


def get_policy(data=None, json=None, method="GET"):
    url = base_url
    if data is None:
        url = base_url + "/listpolicy"
    elif "policyId" in data:
        url = base_url

    policy = requestors.request(url=url, data=data, json=json, method=method)

    try:
        policy_data = policy["data"]
    except Exception:
        log_utils.log_err(policy["status_message"])
    else:
        return policy_data


def buckets_policy(data=None, json=None, method="GET"):
    bucket_policy = requestors.request(
        url=base_url + "/bucketsperpolicy", data=data, json=json, method=method
    )

    try:
        bucket_policy_data = bucket_policy["data"]
    except Exception:
        log_utils.log_err(bucket_policy["status_message"])
    else:
        return bucket_policy_data
