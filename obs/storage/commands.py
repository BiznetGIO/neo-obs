import click
import sys

from obs.libs import auth
from obs.storage import bucket
from obs.storage import gmt
from obs.libs import utils


def warn_inexsit_config():
    msg = (
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one"
    )
    click.secho(msg, fg="yellow", bold=True, err=True)


def get_resources():
    try:
        s3_resource = auth.resource()
        return s3_resource
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)
        warn_inexsit_config()
        sys.exit(1)


def get_plain_auth():
    try:
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
    bucket.create_bucket(
        auth=plain_auth,
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
@click.argument("src_bucket", default="")
@click.argument("dest_bucket", default="")
@click.argument("object_name", default="")
def copy_object(src_bucket, dest_bucket, object_name):
    """Copy object to other bucket."""
    s3_resource = get_resources()
    bucket.copy_object(
        s3_resource,
        src_bucket=src_bucket,
        dest_bucket=dest_bucket,
        object_name=object_name,
    )


@storage.command("mv")
@click.argument("src_bucket", default="")
@click.argument("dest_bucket", default="")
@click.argument("object_name", default="")
def move_object(src_bucket, dest_bucket, object_name):
    """Move object into other bucket."""
    s3_resource = get_resources()
    bucket.move_object(
        s3_resource,
        src_bucket=src_bucket,
        dest_bucket=dest_bucket,
        object_name=object_name,
    )


@storage.command("du")
@click.argument("bucket_name", default="", required=False)
def du(bucket_name):
    """Show disk or bucket usage."""
    s3_resource = get_resources()
    if bucket_name:
        bucket.bucket_usage(s3_resource, bucket_name=bucket_name)
    else:
        bucket.disk_usage(s3_resource)


@storage.command("info")
@click.argument("uri", nargs=-1)
def info(uri):
    """Display bucket or object info."""
    s3_resource = get_resources()
    plain_auth = get_plain_auth()
    if len(target_name) == 1:
        bucket_name = target_name[0]
        bucket.bucket_info(s3_resource, bucket_name=bucket_name, auth=plain_auth)
    if len(target_name) == 2:
        bucket_name, object_name = target_name
        bucket.object_info(
            s3_resource, bucket_name=bucket_name, object_name=object_name
        )


@storage.command("acl")
@click.argument("target_name", nargs=-1)
@click.argument("acl", default="private")
def set_acl(target_name, acl):
    """Set ACL for bucket or object."""
    s3_resource = get_resources()
    if len(target_name) == 1:
        acl_type = "bucket"
        bucket_name = target_name[0]
        bucket.set_acl(
            resource=s3_resource, bucket_name=bucket_name, acl=acl, acl_type=acl_type
        )

    if len(target_name) == 2:
        acl_type = "object"
        bucket_name, object_name = target_name
        bucket.set_acl(
            resource=s3_resource,
            bucket_name=bucket_name,
            object_name=object_name,
            acl=acl,
            acl_type=acl_type,
        )


@storage.command("presign")
@click.argument("target_name", nargs=-1)
@click.option("--expire", "expire", type=int, help="Set expiration time [default:3600]")
def url(target_name, expire):
    """Generate Url for bucket or object."""
    s3_resource = get_resources()
    if len(target_name) == 2:
        bucket_name, object_name = target_name
        bucket.generate_url(
            resource=s3_resource,
            bucket_name=bucket_name,
            object_name=object_name,
            expire=expire,
        )


@storage.command("mkdir")
@click.argument("target_name", nargs=-1)
def mkdir(target_name):
    """Create directory inside bucket"""
    s3_resource = get_resources()
    bucket_name, dir_name = target_name
    bucket.mkdir(resource=s3_resource, bucket_name=bucket_name, dir_name=dir_name)


@storage.command("gmt")
@click.option("--policy-id", "policy_id", is_flag=True, help="List Gmt Policy ID")
def gmt_cmd(policy_id):
    """Manage Cloudian extensions to S3."""
    if policy_id:
        gmt.show_policies()
