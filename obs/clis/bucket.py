import click

from obs.libs import bucket as bucket_lib
from obs.libs import utils


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


def delete_bucket(resource, bucket_name):
    is_deleted, exc = bucket_lib.delete_bucket(resource, bucket_name)
    if is_deleted:
        click.secho(f'Bucket "{bucket_name}" deleted successfully.', fg="green")
    else:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


def get_objects(resource, bucket_name):
    objects, exc = bucket_lib.get_objects(resource, bucket_name)
    if objects:
        for obj in objects:
            key = obj.key
            size = utils.sizeof_fmt(obj.size)
            click.secho(f"{obj.last_modified:%Y-%m-%d %H:%M:%S}, {size}, {key}")
    else:
        click.secho(str(exc), fg="yellow", bold=True, err=True)
