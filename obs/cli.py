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
@click.option("--ls", is_flag=True, default=False, help="List all buckets")
@click.option("--mb", "--make-bucket", default="", help="Make a bucket")
@click.option(
    "-r", "--random", "random_name", is_flag=True, help="Generate random name"
)
@click.option("-del", "--delete", "_del", default="", help="Delete a bucket")
def storage(ls, mb, random_name, _del):
    """Manage user storage."""
    try:
        s3_resource = auth.resource()
        if ls:
            bucket.buckets(s3_resource)
        if mb:
            bucket.create_bucket(s3_resource, bucket_name=mb, random_name=random_name)
        if _del:
            bucket.delete_bucket(s3_resource, bucket_name=_del)

    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


if __name__ == "__main__":
    cli()
