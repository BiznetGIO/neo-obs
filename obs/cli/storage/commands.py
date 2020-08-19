import click
import sys

from obs.libs import auth
from obs.cli.storage import bucket
from obs.cli.storage import gmt
from obs.libs import utils
from obs.libs import config


def warn_inexsit_config():
    msg = (
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one"
    )
    click.secho(msg, fg="yellow", bold=True, err=True)


def get_resources():
    try:
        config.load_config_file()
        s3_resource = auth.resource()
        return s3_resource
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)
        warn_inexsit_config()
        sys.exit(1)


def get_plain_auth():
    try:
        config.load_config_file()
        plain_auth = auth.plain_auth()
        return plain_auth
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)
        warn_inexsit_config()
        sys.exit(1)


@click.group()
def storage():
    """Manage user storage."""


@storage.command("ls")
@click.argument("uri", default="", required=False)
def list(uri):
    """List bucket or object."""
    s3_resource = get_resources()
    if uri:
        bucket.get_objects(s3_resource, uri=uri)
    else:
        bucket.buckets(s3_resource)


@storage.command("rm")
@click.argument("uri")
def remove(uri):
    """Remove bucket or object."""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    if not prefix:
        bucket.remove_bucket(s3_resource, bucket_name=bucket_name)
    if bucket_name and prefix:
        bucket.remove_object(s3_resource, bucket_name=bucket_name, object_name=prefix)


@storage.command("mb")
@click.argument("bucket_name", default="")
@click.option(
    "--acl", "acl", default="private", required=False, help="Access Control List"
)
@click.option(
    "--policy-id",
    "policy_id",
    default="",
    required=False,
    help="Data distribution in bucket",
)
@click.option(
    "-r",
    "--random",
    "random_name",
    default=False,
    is_flag=True,
    help="Generate random name",
)
def make_bucket(bucket_name, acl, policy_id, random_name):
    """Create bucket."""
    plain_auth = get_plain_auth()
    s3_resource = get_resources()
    bucket.create_bucket(
        auth=plain_auth,
        resource=s3_resource,
        bucket_name=bucket_name,
        acl=acl,
        policy_id=policy_id,
        random_name=random_name,
    )


@storage.command("get")
@click.argument("uri")
def get_object(uri):
    """Download object in bucket."""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)
    bucket.download_object(s3_resource, bucket_name=bucket_name, object_name=prefix)


@storage.command("put")
@click.argument("local_path", default="")
@click.argument("uri")
def put_object(local_path, uri):
    """Upload object to bucket."""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)
    bucket.upload_object(
        resource=s3_resource,
        bucket_name=bucket_name,
        local_path=local_path,
        object_name=prefix,
    )


@storage.command("cp")
@click.argument("src_uri", default="")
@click.argument("dest_uri", default="")
def copy_object(src_uri, dest_uri):
    """Copy object to other bucket."""
    s3_resource = get_resources()

    src_bucket, src_prefix = utils.get_bucket_key(src_uri)
    dest_bucket, dest_prefix = utils.get_bucket_key(dest_uri)
    bucket.copy_object(s3_resource, src_bucket, src_prefix, dest_bucket, dest_prefix)


@storage.command("mv")
@click.argument("src_uri", default="")
@click.argument("dest_uri", default="")
def move_object(src_uri, dest_uri):
    """Move object into other bucket."""
    s3_resource = get_resources()

    src_bucket, src_prefix = utils.get_bucket_key(src_uri)
    dest_bucket, dest_prefix = utils.get_bucket_key(dest_uri)

    bucket.move_object(s3_resource, src_bucket, src_prefix, dest_bucket, dest_prefix)


@storage.command("du")
@click.argument("uri", default="", required=False)
def du(uri):
    """Show disk or bucket usage."""
    s3_resource = get_resources()

    bucket_name, prefix = utils.get_bucket_key(uri)
    if bucket_name:
        bucket.bucket_usage(s3_resource, bucket_name=bucket_name)
    else:
        bucket.disk_usage(s3_resource)


@storage.command("info")
@click.argument("uri")
def info(uri):
    """Display bucket or object info."""
    s3_resource = get_resources()
    plain_auth = get_plain_auth()

    bucket_name, prefix = utils.get_bucket_key(uri)
    if not prefix:
        bucket.bucket_info(s3_resource, bucket_name=bucket_name, auth=plain_auth)
    if bucket_name and prefix:
        bucket.object_info(s3_resource, bucket_name=bucket_name, object_name=prefix)


@storage.command("acl")
@click.argument("uri")
@click.argument("acl", default="private")
def set_acl(uri, acl):
    """Set ACL for bucket or object."""
    s3_resource = get_resources()

    bucket_name, prefix = utils.get_bucket_key(uri)
    if not prefix:
        bucket.set_acl(
            resource=s3_resource, bucket_name=bucket_name, acl=acl, acl_type="bucket"
        )
    if bucket_name and prefix:
        bucket.set_acl(
            resource=s3_resource,
            bucket_name=bucket_name,
            object_name=prefix,
            acl=acl,
            acl_type="object",
        )


@storage.command("presign")
@click.argument("uri")
@click.option("--expire", "expire", type=int, help="Set expiration time [default:3600]")
def url(uri, expire):
    """Generate presign URL for object."""
    s3_resource = get_resources()

    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)
    bucket.generate_url(
        resource=s3_resource, bucket_name=bucket_name, object_name=prefix, expire=expire
    )


@storage.command("mkdir")
@click.argument("uri")
def mkdir(uri):
    """Create directory inside bucket"""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    bucket.mkdir(resource=s3_resource, bucket_name=bucket_name, dir_name=prefix)


@storage.command("gmt")
@click.option("--policy-id", "policy_id", is_flag=True, help="List Gmt Policy ID")
def gmt_cmd(policy_id):
    """Manage Cloudian extensions to S3."""
    if policy_id:
        config.load_config_file()
        gmt.show_policies()


@storage.group()
def mpu():
    """Manage multipart upload function"""


@mpu.command("ls")
@click.argument("uri")
def list_mpu(uri):
    """List in-progress multipart uploads"""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    bucket.list_multipart_upload(
        resource=s3_resource, bucket_name=bucket_name, prefix=prefix
    )


@mpu.command("part")
@click.argument("uri")
@click.argument("upload_id")
def list_part(uri, upload_id):
    """List in-progress part in multipart upload"""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    bucket.list_part(
        resource=s3_resource,
        bucket_name=bucket_name,
        object_name=prefix,
        upload_id=upload_id,
    )


@mpu.command("abort")
@click.argument("uri")
@click.argument("upload_id")
def abort_mpu(uri, upload_id):
    """Abort in-progress multipart upload"""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    bucket.abort_multipart_upload(
        resource=s3_resource,
        bucket_name=bucket_name,
        object_name=prefix,
        upload_id=upload_id,
    )


@mpu.command("complete")
@click.argument("uri")
@click.argument("upload_id")
def abort_mpu(uri, upload_id):
    """Complete a multipart upload by assembling uploaded parts"""
    s3_resource = get_resources()
    bucket_name, prefix = utils.get_bucket_key(uri)

    bucket.complete_multipart_upload(
        resource=s3_resource,
        bucket_name=bucket_name,
        object_name=prefix,
        upload_id=upload_id,
    )
