import click

from obs.libs import config as config_lib
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
@click.argument("ls", required=False)
def storage(ls):
    """Manage user storage."""
    try:
        if ls:
            s3_resource = auth.resource()
            bucket.buckets(s3_resource)

    except Exception as e:
        click.secho(
            'Can\'t find config file.\nPlease run "obs --configure".', fg="yellow"
        )
        print(e)


if __name__ == "__main__":
    cli()
