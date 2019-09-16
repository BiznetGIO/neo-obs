import click

from obs.libs import bucket as bucket_lib
from obs.libs import utils


def buckets(resource):
    """Print all bucket with specified attribute."""
    all_buckets = bucket_lib.buckets(resource)
    for bucket in all_buckets:
        click.secho(f"{bucket.creation_date:%Y-%m-%d %H:%M:%S} {bucket.name}")


def create_bucket(resource, bucket_name, acl, random_name=False):
    try:
        bucket_lib.create_bucket(resource, bucket_name, acl, random_name)
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


def get_objects(resource, bucket_name, prefix):
    try:
        objects = bucket_lib.get_objects(resource, bucket_name, prefix)
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


def download_object(resource, bucket_name, object_name):
    try:
        bucket_lib.download_object(resource, bucket_name, object_name)
        click.secho(f'Object "{object_name}" downloaded successfully', fg="green")
    except Exception as exc:
        click.secho(
            f"Object download failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def upload_object(**kwargs):
    try:
        bucket_lib.upload_object(**kwargs)
        click.secho(f"Object uploaded successfully", fg="green")
    except Exception as exc:
        click.secho(f"Object upload failed. \n{exc}", fg="yellow", bold=True, err=True)


def copy_object(resource, src_bucket, dest_bucket, object_name):
    try:
        bucket_lib.copy_object(resource, src_bucket, dest_bucket, object_name)
        click.secho(f'Object "{object_name}" copied successfully', fg="green")
    except Exception as exc:
        click.secho(f"Object copying failed. \n{exc}", fg="yellow", bold=True, err=True)


def disk_usage(resource, bucket_name):
    try:
        total_size, total_objects = bucket_lib.disk_usage(resource, bucket_name)
        human_total_size = utils.sizeof_fmt(total_size)
        click.secho(
            f'{human_total_size}, {total_objects} objects of "{bucket_name}" bucket'
        )
    except Exception as exc:
        click.secho(f"Object copying failed. \n{exc}", fg="yellow", bold=True, err=True)


def move_object(resource, src_bucket, dest_bucket, object_name):
    try:
        bucket_lib.move_object(resource, src_bucket, dest_bucket, object_name)
        click.secho(
            f'Object "{object_name}" moved to "{dest_bucket}" bucket successfully',
            fg="green",
        )
    except Exception as exc:
        click.secho(f"Object moving failed. \n{exc}", fg="yellow", bold=True, err=True)
