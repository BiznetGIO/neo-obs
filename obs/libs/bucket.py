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
