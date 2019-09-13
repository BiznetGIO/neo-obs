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
    resource.create_bucket(Bucket=bucket_name)


def remove_bucket(resource, bucket_name):
    """Remove a bucket."""
    resource.Bucket(bucket_name).delete()


def get_objects(resource, bucket_name):
    """List objects inside a bucket"""
    objects = []
    bucket = resource.Bucket(bucket_name)
    for obj in bucket.objects.all():
        objects.append(obj)
    return objects


def remove_object(resource, bucket_name, object_name):
    """Remove an object in a bucket."""
    objects = get_objects(resource, bucket_name)
    if object_name in [x.key for x in objects]:
        resource.Object(bucket_name, object_name).delete()
    else:
        raise ValueError(f"Object not exists: {object_name}")
