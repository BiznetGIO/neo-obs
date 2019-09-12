import uuid


def buckets(resource):
    """Return all available buckets object."""
    all_buckets = []
    for bucket in resource.buckets.all():
        all_buckets.append(bucket)
    return all_buckets


def gen_random_name(prefix):
    """Take random UUID and append specified prefix."""
    return f"{prefix}-{str(uuid.uuid4())[:13]}"


def create_bucket(resource, bucket_name, random_name=False):
    """Create a bucket with optional random name as a suffix."""
    if random_name:
        bucket_name = gen_random_name(bucket_name)
    is_created = resource.create_bucket(Bucket=bucket_name)
    return is_created, bucket_name


def delete_bucket(resource, bucket_name):
    """Delete a bucket."""
    try:
        resource.Bucket(bucket_name).delete()
        return True, None
    except Exception as exc:
        return False, exc


def get_objects(resource, bucket_name):
    """List objects inside a bucket"""
    try:
        objects = []
        bucket = resource.Bucket(bucket_name)
        for obj in bucket.objects.all():
            objects.append(obj)
        return objects, True
    except Exception as exc:
        return exc, False
