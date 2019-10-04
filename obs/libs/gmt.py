import os
import yaml
import errno
import requests

from obs.libs import config


def policies_file():
    config.load_config_file()
    policy_file = os.environ.get("OBS_USER_GMT_POLICY")
    return policy_file


def is_policy_exists():
    policy_file = policies_file()
    return os.path.isfile(policy_file)


def get_policies():
    """Get policies."""
    policy_file = policies_file()
    if policy_file != "notset" and is_policy_exists():
        policies = yaml.safe_load(open(policy_file))
        return policies
    else:
        return "notset"


def policy_id(bucket_name, auth):
    """Get GMT-Policy id from S3 API response headers."""
    auth, endpoint = auth

    endpoint = f"http://{bucket_name}.{endpoint}"
    response = requests.get(endpoint, auth=auth)
    policy_id = response.headers.get("x-gmt-policyid")

    return policy_id


def policy_description(policy_id):
    """Get GMT-Policy description."""
    policies = get_policies()
    # id not found also will return None
    # so gmt policy will not be shown
    description = None

    if policies == "notset":
        return

    for zone in policies:
        policyid, _description, _ = policies[zone].values()
        if policyid == policy_id:
            description = _description
            break

    if description == "":
        description = "No description"

    return description
