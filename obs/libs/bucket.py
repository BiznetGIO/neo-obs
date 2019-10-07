import uuid
import os
import requests

from obs.libs import gmt


def buckets(resource):
    """Return all available buckets object."""
    all_buckets = []
    for bucket in resource.buckets.all():
        all_buckets.append(bucket)
    return all_buckets


def gen_random_name(prefix):
    """Take random UUID and append specified prefix."""
    return f"{prefix}-{str(uuid.uuid4())[:13]}"


def create_bucket(**kwargs):
    """Create a bucket.

    :param auth: Tuple, consists of auth object and endpoint string
    :param acl: Input for canned ACL, defaults to "private"
    :param policy_id: String represent `x-gmt-policyid` or determines how data in the bucket will be distributed, defaults to None
    :param bucket_name: Bucket name
    :param random: A flag for deciding that a bucket name should be suffixed by random string or not, defaults to False
    """
    auth, endpoint = kwargs.get("auth")
    acl = kwargs.get("acl", "private")
    policy_id = kwargs.get("policy_id", "")
    bucket_name = kwargs.get("bucket_name")

    if kwargs.get("random_name"):
        bucket_name = gen_random_name(bucket_name)

    endpoint = f"http://{bucket_name}.{endpoint}"
    headers = {"x-gmt-policyid": policy_id, "x-amz-acl": acl}

    response = requests.put(endpoint, auth=auth, headers=headers)
    return response


def remove_bucket(resource, bucket_name):
    """Remove a bucket."""
    resource.Bucket(bucket_name).delete()


def get_objects(resource, bucket_name, prefix=""):
    """List objects inside a bucket"""
    objects = []
    bucket = resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        objects.append(obj)
    return objects


def is_exists(resource, bucket_name, object_name):
    objects = get_objects(resource, bucket_name)
    if object_name in [x.key for x in objects]:
        return True
    else:
        return False


def remove_object(resource, bucket_name, object_name):
    """Remove an object in a bucket."""
    if is_exists(resource, bucket_name, object_name):
        resource.Object(bucket_name, object_name).delete()
    else:
        raise ValueError(f"Object not exists: {object_name}")


def download_object(resource, bucket_name, object_name):
    """Download an object in a bucket."""
    if is_exists(resource, bucket_name, object_name):
        resource.Object(bucket_name, object_name).download_file(f"{object_name}")
    else:
        raise ValueError(f"Object not exists: {object_name}")


def upload_object(**kwargs):
    """Upload an object into bucket."""
    filename = kwargs.get("path", "")  # use path as default filename
    path = kwargs.get("path")

    if kwargs.get("object_name"):
        filename = kwargs.get("object_name")
    if kwargs.get("use_basename"):
        filename = os.path.basename(path)

    resource = kwargs.get("resource")
    bucket_name = kwargs.get("bucket_name")
    resource.Object(bucket_name, filename).upload_file(Filename=path)


def copy_object(resource, src_bucket, dest_bucket, object_name):
    """Copy an object into other bucket."""
    copy_source = {"Bucket": src_bucket, "Key": object_name}
    resource.Object(dest_bucket, object_name).copy(copy_source)


def move_object(resource, src_bucket, dest_bucket, object_name):
    """Move an object into other bucket.
    Using copy then remove operation.
    """
    copy_object(resource, src_bucket, dest_bucket, object_name)
    remove_object(resource, src_bucket, object_name)


def bucket_usage(resource, bucket_name):
    """Calculate bucket usage."""
    objects = get_objects(resource, bucket_name)
    total_objects = len(objects)
    total_size = 0
    for obj in objects:
        total_size += obj.size
    return total_size, total_objects


def disk_usage(resource):
    """Calculate disk usage."""
    all_buckets = buckets(resource)
    bucket_names = [bucket.name for bucket in all_buckets]

    disk_usages = []
    for bucket_name in bucket_names:
        usage = bucket_usage(resource, bucket_name)
        disk_usages.append([bucket_name, usage])

    return disk_usages


def get_cors(bucket):
    try:
        cors = bucket.Cors().cors_rules
    except Exception:
        cors = None
    return cors


def get_policy(bucket):
    try:
        policy = bucket.Policy().policy
    except Exception:
        policy = None
    return policy


def get_location(client, bucket_name):
    response = client.get_bucket_location(Bucket=bucket_name)
    location = response["LocationConstraint"]
    return location


def get_expiration(client, bucket_name):
    try:
        exp = client.get_bucket_lifecycle(Bucket=bucket_name)
    except Exception:
        exp = None
    return exp


def get_grant_name(grant):
    """Get grant name based on Grantee type."""
    grant_name = ""
    if grant["Grantee"]["Type"] == "Group":
        uri = grant["Grantee"]["URI"]
        grant_name = uri.rsplit("/", 1)[-1]

    if grant["Grantee"]["Type"] == "CanonicalUser":
        grant_name = grant["Grantee"]["DisplayName"]

    return grant_name


def get_grants(obj):
    """Get grants info of bucket or object."""
    grants = obj.Acl().grants
    grantees = []

    for grant in grants:
        name = get_grant_name(grant)
        permission = grant["Permission"]
        grantee = [name, permission]
        grantees.append(grantee)

    return grantees


def bucket_gmt_policy(bucket_name, auth):
    """Get bucket GMT-Policy"""
    policy_id = gmt.policy_id(bucket_name, auth)
    description = gmt.policy_description(policy_id)
    return description


def bucket_info(resource, bucket_name, auth):
    """Info of bucket."""
    bucket = resource.Bucket(bucket_name)
    client = resource.meta.client

    gmt_policy = bucket_gmt_policy(bucket_name, auth)
    info = {
        "ACL": get_grants(bucket),
        "CORS": get_cors(bucket),
        "Policy": get_policy(bucket),
        "Expiration": get_expiration(client, bucket_name),
        "Location": get_location(client, bucket_name),
    }
    if gmt_policy:
        info["GmtPolicy"] = gmt_policy

    return info


def object_info(resource, bucket_name, object_name):
    """Info of object."""
    obj = resource.Object(bucket_name=bucket_name, key=object_name)
    storage_class = obj.storage_class
    content_type = obj.content_type
    grantees = get_grants(obj)

    info = {
        "ACL": grantees,
        "Size": obj.content_length,
        "LastModified": obj.last_modified,
        "MD5": obj.e_tag,
        "MimeType": content_type,
        "StorageClass": storage_class,
    }
    return info


def set_acl(**kwargs):
    """Set ACL of object or object."""
    resource = kwargs.get("resource")
    bucket_name = kwargs.get("bucket_name")
    object_name = kwargs.get("object_name")

    if kwargs.get("acl_type") == "object":
        obj = resource.Object(bucket_name=bucket_name, key=object_name)
    if kwargs.get("acl_type") == "bucket":
        obj = resource.Bucket(bucket_name)

    obj.Acl().put(ACL=kwargs.get("acl"))


def generate_url(resource, bucket_name, object_name, expire=3600):
    """Generate URL for bucket or object."""
    client = resource.meta.client
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expire,
    )
    return url


def mkdir(resource, bucket_name, dir_name):
    """Create directory inside bucket"""
    client = resource.meta.client
    if not dir_name.endswith("/"):
        dir_name = f"{dir_name}/"

    client.put_object(Bucket=bucket_name, Body="", Key=dir_name)
