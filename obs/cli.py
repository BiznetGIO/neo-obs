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
@click.option("--ro", "remove_object", nargs=2, help="Remove object in bucket")
@click.option("--get", "download_object", nargs=2, help="Download object in bucket")
def storage(
    list_bucket,
    make_bucket,
    random_name,
    remove_bucket,
    list_object,
    remove_object,
    download_object,
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

    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


if __name__ == "__main__":
    cli()
