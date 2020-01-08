import click
import bitmath

from obs.libs import bucket as bucket_lib
from obs.libs import utils


def buckets(resource):
    """Print all bucket with specified attribute."""
    try:
        all_buckets = bucket_lib.buckets(resource)
        for bucket in all_buckets:
            click.secho(f"{bucket.creation_date:%Y-%m-%d %H:%M:%S} {bucket.name}")
    except Exception as exc:
        click.secho(f"Bucket listing failed. \n{exc}", fg="yellow", bold=True, err=True)


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


def get_objects(resource, uri):
    try:
        bucket_name, prefix = utils.get_bucket_key(uri)
        response = bucket_lib.get_objects(resource, bucket_name, prefix)
        if not response:
            click.secho(f'Bucket "{bucket_name}" is empty', fg="green")
            return

        if response["CommonPrefixes"]:
            for prefix in response["CommonPrefixes"]:
                dir_ = "DIR".rjust(12)
                click.secho(f"{dir_} {bucket_name}/{prefix['Prefix']}")

        if response["Contents"]:
            for content in response["Contents"]:
                key = content["Key"]
                size = utils.sizeof_fmt(content["Size"])
                last_modified = content["LastModified"]
                click.secho(
                    f"{last_modified:%Y-%m-%d %H:%M:%S}, {size}, {bucket_name}/{key}"
                )

    except Exception as exc:
        click.secho(f"{exc}", fg="yellow", bold=True, err=True)


def remove_object(resource, bucket_name, object_name):
    try:
        bucket_lib.remove_object(resource, bucket_name, object_name)
        click.secho(f'Object "{object_name}" removed successfully', fg="green")
    except Exception as exc:
        click.secho(f"Object removal failed. \n{exc}", fg="yellow", bold=True, err=True)


def download_object(resource, bucket_name, object_name):
    if object_name.endswith("/"):
        click.secho(
            f"Object download failed. \nExpecting filename", fg="yellow", bold=True
        )
        return

    try:
        bucket_lib.download_object(resource, bucket_name, object_name)
        click.secho(f'Object "{object_name}" downloaded successfully', fg="green")
    except Exception as exc:
        click.secho(
            f"Object download failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def upload_object(**kwargs):
    try:
        filename = bucket_lib.upload_object(**kwargs)
        click.secho(f'Object "{filename}" uploaded successfully', fg="green")
    except Exception as exc:
        click.secho(
            f'Object "{filename}" upload failed. \n{exc}',
            fg="yellow",
            bold=True,
            err=True,
        )


def copy_object(resource, src_bucket, src_object_name, dest_bucket, dest_object_name):
    if src_object_name.endswith("/") or not src_object_name:
        click.secho(f"Object copy failed. \nExpecting filename", fg="yellow", bold=True)
        return

    try:
        bucket_lib.copy_object(
            resource, src_bucket, src_object_name, dest_bucket, dest_object_name
        )
        click.secho(f'Object "{src_object_name}" copied successfully', fg="green")
    except Exception as exc:
        click.secho(f"Object copy failed. \n{exc}", fg="yellow", bold=True, err=True)


def bucket_usage(resource, bucket_name):
    try:
        total_size, total_objects = bucket_lib.bucket_usage(resource, bucket_name)
        human_total_size = bitmath.Byte(total_size).best_prefix()
        click.secho(
            f'{human_total_size.format("{value:.2f} {unit}")}, {total_objects} objects in "{bucket_name}" bucket'
        )
    except Exception as exc:
        click.secho(
            f"Bucket usage fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def disk_usage(resource):
    try:
        disk_usages = bucket_lib.disk_usage(resource)
        total_usage = 0
        for usage in disk_usages:
            bucket_name = usage[0]
            total_size, total_objects = usage[1]
            human_total_size = bitmath.Byte(total_size).best_prefix()
            total_usage += total_size
            click.secho(
                f'{human_total_size.format("{value:.2f} {unit}")}, {total_objects} objects in "{bucket_name}" bucket'
            )

        human_total_usage = bitmath.Byte(total_usage).best_prefix()
        click.secho(f"---\n" f"{human_total_usage.format('{value:.2f} {unit}')} Total")

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


def bucket_info(resource, bucket_name, auth):
    try:
        info = bucket_lib.bucket_info(resource, bucket_name, auth)
        msg = (
            f"Location: {info['Location']}\n"
            f"Expiration Rule: {info['Expiration']}\n"
            f"Policy: {info['Policy']}\n"
            f"CORS: {info['CORS']}"
        )
        click.secho(msg)

        for grant in info["ACL"]:
            click.secho(f"ACL: {grant[0]} : {grant[1]}")

        if "GmtPolicy" in info:
            click.secho(f"Gmt Policy: {info['GmtPolicy']}")

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
