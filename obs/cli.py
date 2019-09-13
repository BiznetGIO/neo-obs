import click

from obs.libs import auth

from obs.clis import config
from obs.clis import bucket


@click.group(invoke_without_command=True)
@click.option(
    "--configure",
    is_flag=True,
    default=False,
    help="Configure object storage service values",
)
@click.version_option()
def cli(configure):
    """neo-obs

    Command line tool for neo object storage.
    """
    if configure:
        config.run_configure()


@cli.command()
@click.option("--lb", "list_bucket", is_flag=True, help="List all buckets")
@click.option("--mb", "make_bucket", type=str, help="Make a bucket")
@click.option(
    "-r", "--random", "random_name", is_flag=True, help="Generate random name"
)
@click.option("--rb", "remove_bucket", default="", help="Remove a bucket")
@click.option("--lo", "list_object", default="", help="List bucket's objects")
@click.option("--rm", "remove_object", nargs=2, help="Remove object in bucket")
@click.option("--get", "download_object", nargs=2, help="Download object in bucket")
@click.option("--put", "upload_object", nargs=2, help="Put object into bucket")
@click.option("--cp", "copy_object", nargs=3, help="Copy object to other bucket")
@click.option("--mv", "move_object", nargs=3, help="Move object into other bucket")
@click.option("--du", "disk_usage", default="", help="Disk usage of bucket")
def storage(
    list_bucket,
    make_bucket,
    random_name,
    remove_bucket,
    list_object,
    remove_object,
    download_object,
    upload_object,
    copy_object,
    move_object,
    disk_usage,
):
    """Manage user storage."""
    try:
        s3_resource = auth.resource()
        if list_bucket:
            bucket.buckets(s3_resource)
        if make_bucket:
            bucket.create_bucket(
                s3_resource, bucket_name=make_bucket, random_name=random_name
            )
        if remove_bucket:
            bucket.remove_bucket(s3_resource, bucket_name=remove_bucket)
        if list_object:
            bucket.get_objects(s3_resource, bucket_name=list_object)
        if remove_object:
            bucket_name, object_name = remove_object
            bucket.remove_object(
                s3_resource, bucket_name=bucket_name, object_name=object_name
            )
        if download_object:
            bucket_name, object_name = download_object
            bucket.download_object(
                s3_resource, bucket_name=bucket_name, object_name=object_name
            )
        if upload_object:
            bucket_name, object_name = upload_object
            bucket.upload_object(
                s3_resource, bucket_name=bucket_name, object_name=object_name
            )
        if copy_object:
            src_bucket, dest_bucket, object_name = copy_object
            bucket.copy_object(
                s3_resource,
                src_bucket=src_bucket,
                dest_bucket=dest_bucket,
                object_name=object_name,
            )
        if move_object:
            src_bucket, dest_bucket, object_name = move_object
            bucket.move_object(
                s3_resource,
                src_bucket=src_bucket,
                dest_bucket=dest_bucket,
                object_name=object_name,
            )
        if disk_usage:
            bucket.disk_usage(s3_resource, bucket_name=disk_usage)

    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


if __name__ == "__main__":
    cli()
