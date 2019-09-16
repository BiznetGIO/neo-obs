import click


from obs.storage import config
from obs.storage import commands


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


cli.add_command(commands.storage)

if __name__ == "__main__":
    cli()
