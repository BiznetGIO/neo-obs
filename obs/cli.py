import click

from obs.clis import config
from obs.libs import config as config_lib


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


if __name__ == "__main__":
    cli()
