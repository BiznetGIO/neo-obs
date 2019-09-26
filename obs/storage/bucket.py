import click

from obs.libs import bucket as bucket_lib
from obs.libs import utils


def buckets(resource):
    """Print all bucket with specified attribute."""
    all_buckets = bucket_lib.buckets(resource)
    for bucket in all_buckets:
        click.secho(f"{bucket.creation_date:%Y-%m-%d %H:%M:%S} {bucket.name}")


def create_bucket(**kwargs):
    try:
        response = bucket_lib.create_bucket(**kwargs)
        utils.check_plain(response)
        click.secho(
            f'Bucket "{kwargs.get("bucket_name")}" created successfully', fg="green"
        )
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
        click.secho(
            f"Disk usage fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def move_object(resource, src_bucket, dest_bucket, object_name):
    try:
        bucket_lib.move_object(resource, src_bucket, dest_bucket, object_name)
        click.secho(
            f'Object "{object_name}" moved to "{dest_bucket}" bucket successfully',
            fg="green",
        )
    except Exception as exc:
        click.secho(f"Object moving failed. \n{exc}", fg="yellow", bold=True, err=True)


def bucket_info(resource, bucket_name):
    try:
        info = bucket_lib.bucket_info(resource, bucket_name)
        msg = (
            f"Location: {info['Location']}\n"
            f"Expiration Rule: {info['Expiration']}\n"
            f"Policy: {info['Policy']}\n"
            f"CORS: {info['CORS']}"
        )
        click.secho(msg)
        for grant in info["ACL"]:
            click.secho(f"ACL: {grant[0]} : {grant[1]}")

    except Exception as exc:
        click.secho(f"Info fetching failed. \n{exc}", fg="yellow", bold=True, err=True)


def object_info(resource, bucket_name, object_name):
    try:
        info = bucket_lib.object_info(resource, bucket_name, object_name)
        size = utils.sizeof_fmt(info["Size"])
        last_modified = f"{info['LastModified']:%Y-%m-%d %H:%M:%S}"

        msg = (
            f"File Size: {size}\n"
            f"Last Modified: {last_modified}\n"
            f"Mime Type: {info['MimeType']}\n"
            f"Storage: {info['StorageClass']}\n"
            f"MD5 Sum: {info['MD5']}"
        )
        click.secho(msg)
        for grant in info["ACL"]:
            click.secho(f"ACL: {grant[0]} : {grant[1]}")
    except Exception as exc:
        click.secho(f"Info fetching failed. \n{exc}", fg="yellow", bold=True, err=True)


def set_acl(**kwargs):
    try:
        bucket_lib.set_acl(**kwargs)
        click.secho(f"ACL changed successfully", fg="green")
    except Exception as exc:
        click.secho(f"ACL change failed. \n{exc}", fg="yellow", bold=True, err=True)


def generate_url(resource, bucket_name, object_name, expire):
    try:
        url = bucket_lib.generate_url(resource, bucket_name, object_name, expire)
        click.secho(f"{url}")
    except Exception as exc:
        click.secho(f"URL generation failed. \n{exc}", fg="yellow", bold=True, err=True)


def mkdir(resource, bucket_name, dir_name):
    try:
        bucket_lib.mkdir(resource, bucket_name, dir_name)
        click.secho(f'Directory "{dir_name}" created successfully', fg="green")
    except Exception as exc:
        click.secho(
            f"Directory creation failed. \n{exc}", fg="yellow", bold=True, err=True
        )
