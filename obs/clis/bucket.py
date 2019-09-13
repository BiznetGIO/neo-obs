import click

from obs.libs import bucket as bucket_lib
from obs.libs import utils


def buckets(resource):
    """Print all bucket with specified attribute."""
    all_buckets = bucket_lib.buckets(resource)
    for bucket in all_buckets:
        click.secho(f"{bucket.creation_date:%Y-%m-%d %H:%M:%S} {bucket.name}")


def create_bucket(resource, bucket_name, random_name=False):
    try:
        bucket_lib.create_bucket(resource, bucket_name, random_name)
        click.secho(f'Bucket "{bucket_name}" created successfully', fg="green")
    except Exception as exc:
        click.secho(
            f"Bucket creation failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def remove_bucket(resource, bucket_name):
    try:
        bucket_lib.remove_bucket(resource, bucket_name)
        click.secho(f'Bucket "{bucket_name}" deleted successfully.', fg="green")
    except Exception as exc:
        click.secho(f"{exc}", fg="yellow", bold=True, err=True)


def get_objects(resource, bucket_name):
    try:
        objects = bucket_lib.get_objects(resource, bucket_name)
        if len(objects) > 0:
            for obj in objects:
                key = obj.key
                size = utils.sizeof_fmt(obj.size)
                click.secho(f"{obj.last_modified:%Y-%m-%d %H:%M:%S}, {size}, {key}")
        else:
            click.secho(f'Bucket "{bucket_name}" is empty', fg="green")
    except Exception as exc:
        click.secho(f"{exc}", fg="yellow", bold=True, err=True)


def remove_object(resource, bucket_name, object_name):
    try:
        bucket_lib.remove_object(resource, bucket_name, object_name)
        click.secho(f'Object "{object_name}" removed successfully', fg="green")
    except Exception as exc:
        click.secho(f"Object removal failed. \n{exc}", fg="yellow", bold=True, err=True)
