import re
import os
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
        regex = r"[^a-z0-9.-]"
        name = re.sub(regex, "", kwargs.pop("bucket_name"))
        if not 2 < len(name) < 64:
            raise ValueError(f"'{name}' too short or too long for bucket name")

        if utils.compatibility():
            response = bucket_lib.neo_create_bucket(**kwargs, bucket_name=name)
            utils.check_plain(response)
        else:
            response = bucket_lib.create_bucket(**kwargs, bucket_name=name)
        click.secho(f'Bucket "{name}" created successfully', fg="green")
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
    try:
        objects = bucket_lib.list_download(resource, bucket_name, object_name)
        if object_name == "":
            os.makedirs(bucket_name, exist_ok=True)
            os.chdir(bucket_name)
            name = f'Bucket "{bucket_name}"'
        elif object_name[-1] == "/":
            name = f'Directory "{object_name}"'
        else:
            name = f'Object "{object_name}"'
            objects = [object_name]
        for obj in objects:
            bucket_lib.download_object(resource, bucket_name, obj)
        click.secho(f"{name} downloaded successfully", fg="green")
    except Exception as exc:
        click.secho(
            f"Object download failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def upload_object(**kwargs):
    filename = kwargs.get("local_path")
    try:
        regex = r"[\"\{}^%`\]\[~<>|#]|[^\x00-\x7F]"
        name = re.sub(regex, "", kwargs.pop("object_name"))

        bucket_lib.upload_object(**kwargs, object_name=name)
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


def move_object(resource, src_bucket, src_object_name, dest_bucket, dest_object_name):
    if src_object_name.endswith("/") or not src_object_name:
        click.secho(f"Object move failed. \nExpecting filename", fg="yellow", bold=True)
        return

    try:
        bucket_lib.move_object(
            resource, src_bucket, src_object_name, dest_bucket, dest_object_name
        )

        click.secho(
            f'Object "{src_object_name}" moved to "{dest_bucket}" bucket successfully',
            fg="green",
        )
    except Exception as exc:
        click.secho(f"Object move failed. \n{exc}", fg="yellow", bold=True, err=True)


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


def list_multipart_upload(resource, bucket_name, prefix):
    try:
        response = bucket_lib.list_multipart_upload(resource, bucket_name, prefix)

        if response["CommonPrefixes"]:
            for prefix in response["CommonPrefixes"]:
                dir_ = "DIR".rjust(12)
                click.secho(f"{dir_} {bucket_name}/{prefix['Prefix']}")

        if response["Uploads"]:
            for content in response["Uploads"]:
                key = content["Key"]
                uid = content["UploadId"]
                last_modified = content["Initiated"]
                click.secho(
                    f"{last_modified:%Y-%m-%d %H:%M:%S}, {uid}, {bucket_name}/{key}"
                )

    except Exception as exc:
        click.secho(f"{exc}", fg="yellow", bold=True, err=True)


def list_part(resource, bucket_name, object_name, upload_id):
    try:
        response = bucket_lib.list_part(resource, bucket_name, object_name, upload_id)

        for part in response:
            size = utils.sizeof_fmt(part["Size"])
            last_modified = f"{part['LastModified']:%Y-%m-%d %H:%M:%S}"
            msg = (
                f'Number of part: {part["PartNumber"]}\n'
                f"Last Modified: {last_modified}\n"
                f'ETag: {part["ETag"]}\n'
                f"Size: {size}"
            )
            click.secho(msg)

    except Exception as exc:
        click.secho(f"{exc}", fg="yellow", bold=True, err=True)


def abort_multipart_upload(resource, bucket_name, object_name, upload_id):
    try:
        bucket_lib.abort_multipart_upload(resource, bucket_name, object_name, upload_id)
        click.secho(
            f'Multipart Upload of "{object_name}" aborted successfully', fg="green"
        )
    except Exception as exc:
        click.secho(
            f'Aborting multipart upload of "{object_name}" failed.\n{exc}',
            fg="yellow",
            bold=True,
            err=True,
        )


def complete_multipart_upload(resource, bucket_name, object_name, upload_id):
    try:
        bucket_lib.complete_multipart_upload(
            resource, bucket_name, object_name, upload_id
        )
        click.secho(
            f'Multipart Upload of "{object_name}" completed successfully', fg="green"
        )
    except Exception as exc:
        click.secho(
            f'Completing multipart upload of "{object_name}" failed.\n{exc}',
            fg="yellow",
            bold=True,
            err=True,
        )
