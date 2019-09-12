def buckets(resource):
    """Return all available buckets object."""
    all_buckets = []
    for bucket in resource.buckets.all():
        all_buckets.append(bucket)
    return all_buckets
