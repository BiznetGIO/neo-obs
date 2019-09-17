import click


from obs.storage import config
from obs.storage import commands
from obs.admin import commands as commands_admin


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
cli.add_command(commands_admin.admin)

if __name__ == "__main__":
    cli()
