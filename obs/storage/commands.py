import click

from obs.libs import auth
from obs.storage import bucket


def get_resources():
    try:
        s3_resource = auth.resource()
        return s3_resource
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


@click.group()
def storage():
    """Manage user storage."""


@storage.command("ls")
@click.argument("bucket_name", default="", required=False)
@click.option("-p", "prefix", default="", help="Prefix location")
def list(bucket_name, prefix):
    """List bucket or object."""
    s3_resource = get_resources()
    if bucket_name:
        bucket.get_objects(s3_resource, bucket_name=bucket_name, prefix=prefix)
    else:
        bucket.buckets(s3_resource)


@storage.command("rm")
@click.argument("target_name", nargs=-1)
def remove(target_name):
    """Remove bucket or object."""
    s3_resource = get_resources()
    if len(target_name) == 1:
        bucket.remove_bucket(s3_resource, bucket_name=target_name[0])
    if len(target_name) == 2:
        bucket_name, object_name = target_name
        bucket.remove_object(
            s3_resource, bucket_name=bucket_name, object_name=object_name
        )


@storage.command("mb")
@click.argument("bucket_name", default="")
@click.option(
    "--acl", "acl", default="private", required=False, help="Access Control List"
)
@click.option(
    "-r",
    "--random",
    "random_name",
    default=False,
    is_flag=True,
    help="Generate random name",
)
def make_bucket(bucket_name, acl, random_name):
    """Create bucket."""
    s3_resource = get_resources()
    bucket.create_bucket(
        s3_resource, bucket_name=bucket_name, acl=acl, random_name=random_name
    )


@storage.command("get")
@click.argument("bucket_name", default="")
@click.argument("object_name", default="")
def get_object(bucket_name, object_name):
    """Download object in bucket."""
    s3_resource = get_resources()
    bucket.download_object(
        s3_resource, bucket_name=bucket_name, object_name=object_name
    )


@storage.command("put")
@click.argument("bucket_name", default="")
@click.argument("path", default="")
@click.argument("object_name", default="", required=False)
@click.option(
    "--use-basename",
    "use_basename",
    default=False,
    is_flag=True,
    help="Use basename for object name",
)
def put_object(bucket_name, path, object_name, use_basename):
    s3_resource = get_resources()
    bucket.upload_object(
        resource=s3_resource,
        bucket_name=bucket_name,
        path=path,
        object_name=object_name,
        use_basename=use_basename,
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
@click.argument("bucket_name", default="")
def disk_usage(bucket_name):
    """Disk usage of bucket."""
    s3_resource = get_resources()
    bucket.disk_usage(s3_resource, bucket_name=bucket_name)
