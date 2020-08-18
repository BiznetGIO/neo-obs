import uuid
import os
import requests
import logging
import zipfile

from obs.libs import gmt
from obs.libs import utils
from obs.libs import auth as auth_lib


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
    """Create a bucket."""
    resource = kwargs.get("resource")
    acl = kwargs.get("acl", "private")
    bucket_name = kwargs.get("bucket_name")

    if kwargs.get("random_name"):
        bucket_name = gen_random_name(bucket_name)

    response = resource.Bucket(bucket_name).create(ACL=acl)
    return response


def neo_create_bucket(**kwargs):
    """Create a bucket with headers.

    :param auth: Tuple, consists of auth object and endpoint string
    :param acl: Input for canned ACL, defaults to "private"
    :param policy_id: String represent `x-gmt-policyid` or determines how data in the bucket will be distributed, defaults to None
    :param bucket_name: Bucket name
    :param random: A flag for deciding that a bucket name should be suffixed by random string or not, defaults to False
    """
    auth = kwargs.get("auth")
    acl = kwargs.get("acl", "private")
    policy_id = kwargs.get("policy_id", "")
    bucket_name = kwargs.get("bucket_name")

    if kwargs.get("random_name"):
        bucket_name = gen_random_name(bucket_name)

    endpoint = auth_lib.get_endpoint("storage", bucket_name)
    headers = {"x-gmt-policyid": policy_id, "x-amz-acl": acl}

    response = requests.put(endpoint, auth=auth, headers=headers)
    return response


def remove_bucket(resource, bucket_name):
    """Remove a bucket."""
    response = resource.Bucket(bucket_name).delete()
    return response


def get_objects(resource, bucket_name, prefix=""):
    """List objects inside a bucket"""
    client = resource.meta.client
    next_token = ""
    content = []
    directory = []
    add_list = lambda keys, values: keys.extend(values) if values is not None else None

    while True:
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            Delimiter="/",
            ContinuationToken=next_token,
        )
        add_list(content, response.get("Contents"))
        add_list(directory, response.get("CommonPrefixes"))
        next_token = response.get("NextContinuationToken")

        if next_token is None:
            return {"Contents": content, "CommonPrefixes": directory}


def get_files(resource, bucket_name, prefix=""):
    """List only files inside a bucket (DIR excluded)."""
    files = []
    bucket = resource.Bucket(bucket_name)
    for file_ in bucket.objects.filter(Prefix=prefix):
        files.append(file_)
    return files


def is_exists(resource, bucket_name, object_name):
    response = get_objects(resource, bucket_name, prefix=object_name)
    if not response["Contents"]:
        return False

    if object_name in [x["Key"] for x in response["Contents"]]:
        return True
    else:
        return False


def remove_object(resource, bucket_name, object_name):
    """Remove an object in a bucket."""
    if is_exists(resource, bucket_name, object_name):
        response = resource.Object(bucket_name, object_name).delete()
        return response
    else:
        raise ValueError(f"Object not exists: {object_name}")


def download_object(resource, bucket_name, object_name):
    """Download an object in a bucket."""
    if not is_exists(resource, bucket_name, object_name):
        raise ValueError(f"Object not exists: {object_name}")

    if os.path.dirname(object_name):
        # if object contains '/'
        os.makedirs(os.path.dirname(object_name), exist_ok=True)
    resource.Object(bucket_name, object_name).download_file(f"{object_name}")


def list_download(resources, bucket_name, prefix, list_objects=None):
    """List of objects to download"""
    if list_objects is None:
        list_objects = []

    status = get_objects(resources, bucket_name, prefix)
    for obj in status["Contents"]:
        if obj["Key"][-1] != "/":
            list_objects.append(obj["Key"])
    for dir in status["CommonPrefixes"]:
        list_download(resources, bucket_name, dir["Prefix"], list_objects)
    return list_objects


def upload_object(**kwargs):
    """Upload an object into bucket."""
    # use local filename if not supplied
    filename = kwargs.get("local_path", "")
    local_path = kwargs.get("local_path")

    if kwargs.get("object_name"):
        filename = kwargs.get("object_name")

    resource = kwargs.get("resource")
    bucket_name = kwargs.get("bucket_name")
    resource_upload = resource.Object(bucket_name, filename)
    if kwargs.get("content_type"):
        resource_upload.upload_file(
            Filename=local_path, ExtraArgs={"ContentType": kwargs.get("content_type")}
        )
    else:
        resource_upload.upload_file(Filename=local_path)


def upload_bin_object(**kwargs):
    """Upload an binary object into bucket."""
    fileobj = kwargs.get("fileobj")
    filename = kwargs.get("object_name")

    resource = kwargs.get("resource")
    bucket_name = kwargs.get("bucket_name")
    resource_upload = resource.Object(bucket_name, filename)

    if kwargs.get("content_type"):
        resource_upload.upload_fileobj(
            Fileobj=fileobj, ExtraArgs={"ContentType": kwargs.get("content_type")}
        )
    else:
        resource_upload.upload_fileobj(Fileobj=fileobj)


def list_multipart_upload(resource, bucket_name, prefix=""):
    """List in-progress multipart uploads"""
    client = resource.meta.client
    mpupload = client.list_multipart_uploads(Bucket=bucket_name, Prefix=prefix)

    return {
        "Uploads": mpupload.get("Uploads"),
        "CommonPrefixes": mpupload.get("CommonPrefixes"),
    }


def list_part(resource, bucket_name, object_name, upload_id):
    """List in-progress part in multipart upload"""
    client = resource.meta.client
    mpupload = client.list_parts(
        Bucket=bucket_name, Key=object_name, UploadId=upload_id
    )
    return mpupload.get("Parts")


def abort_multipart_upload(resource, bucket_name, object_name, upload_id):
    """Abort in-progress multipart upload"""
    mpupload = resource.MultipartUpload(bucket_name, object_name, upload_id)
    return mpupload.abort()


def complete_multipart_upload(resource, bucket_name, object_name, upload_id):
    """Complete a multipart upload by assembling uploaded parts"""
    mpupload = resource.MultipartUpload(bucket_name, object_name, upload_id)
    parts = list_part(resource, bucket_name, object_name, upload_id)

    multipart = []
    for part in parts:
        multipart.append(
            {"ETag": part.get("ETag"), "PartNumber": part.get("PartNumber")}
        )
    return mpupload.complete(MultipartUpload={"Parts": multipart})


def copy_object(resource, src_bucket, src_object_name, dest_bucket, dest_object_name):
    """Copy an object into other bucket."""

    if not dest_object_name:
        # use source object name if not supplied
        dest_object_name = src_object_name

    copy_source = {"Bucket": src_bucket, "Key": src_object_name}
    resource.Object(dest_bucket, dest_object_name).copy(copy_source)


def move_object(resource, src_bucket, src_object_name, dest_bucket, dest_object_name):
    """Move an object into other bucket.
    Using copy then remove operation.
    """
    copy_object(resource, src_bucket, src_object_name, dest_bucket, dest_object_name)
    remove_object(resource, src_bucket, src_object_name)


def bucket_usage(resource, bucket_name):
    """Calculate bucket usage."""
    objects = get_files(resource, bucket_name)
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

    response = obj.Acl().put(
        ACL=kwargs.get("acl"),
        GrantFullControl=utils.set_id(kwargs.get("grant_fullcontrol")),
        GrantRead=utils.set_id(kwargs.get("grant_read")),
        GrantReadACP=utils.set_id(kwargs.get("grant_readACP")),
        GrantWrite=utils.set_id(kwargs.get("grant_write")),
        GrantWriteACP=utils.set_id(kwargs.get("grant_writeACP")),
    )
    return response


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

    response = client.put_object(Bucket=bucket_name, Body="", Key=dir_name)
    return response
