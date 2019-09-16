import uuid
import os


def buckets(resource):
    """Return all available buckets object."""
    all_buckets = []
    for bucket in resource.buckets.all():
        all_buckets.append(bucket)
    return all_buckets


def gen_random_name(prefix):
    """Take random UUID and append specified prefix."""
    return f"{prefix}-{str(uuid.uuid4())[:13]}"


def create_bucket(resource, bucket_name, acl="private", random_name=False):
    """Create a bucket with optional random name as a suffix."""
    if random_name:
        bucket_name = gen_random_name(bucket_name)
    resource.create_bucket(Bucket=bucket_name, ACL=acl)


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


def disk_usage(resource, bucket_name):
    """Calculate dist usage of objects in bucket."""
    objects = get_objects(resource, bucket_name)
    total_objects = len(objects)
    total_size = 0
    for obj in objects:
        total_size += obj.size
    return total_size, total_objects


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


def info(resource, bucket_name):
    """Info of bucket."""
    bucket = resource.Bucket(bucket_name)
    client = resource.meta.client
    acl_user = bucket.Acl().grants[0]["Grantee"]["DisplayName"]
    acl_ctrl = bucket.Acl().grants[0]["Permission"]
    expiration = get_expiration(client, bucket_name)
    location = get_location(client, bucket_name)
    policy = get_policy(bucket)
    cors = get_cors(bucket)

    info = {
        "ACL": [acl_user, acl_ctrl],
        "CORS": cors,
        "Policy": policy,
        "Expiration": expiration,
        "Location": location,
    }
    return info
