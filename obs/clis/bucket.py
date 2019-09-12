import click

from obs.libs import bucket as bucket_lib


def buckets(resource):
    """Print all bucket with specified attribute."""
    all_buckets = bucket_lib.buckets(resource)
    for bucket in all_buckets:
        click.secho(f"{bucket.creation_date:%Y-%m-%d %H:%M:%S} {bucket.name}")


def create_bucket(resource, bucket_name, random_name=False):
    is_created, bucket_name = bucket_lib.create_bucket(
        resource, bucket_name, random_name
    )
    if is_created:
        click.secho(f'Bucket "{bucket_name}" created successfully', fg="green")
    else:
        click.secho("Bucket creation failed.", fg="yellow", bold=True, err=True)
