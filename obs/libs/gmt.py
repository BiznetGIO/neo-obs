import os
import yaml
import errno
import requests


def policies_file():
    directory = os.path.dirname(os.path.realpath(__file__))
    policy_file = os.path.join(directory, "gmt_policy.yaml")
    return policy_file


def get_policies():
    """Get policies."""
    policy_file = policies_file()
    if policies_file:
        policies = yaml.safe_load(open(policy_file))
        return policies
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), policy_file)


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

    for zone in policies:
        policyid, description, _ = policies[zone].values()
        if policyid == policy_id:
            break

    return description
