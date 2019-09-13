import os
import dotenv
import errno
import click
import io
import sys


class Config:
    """Accommodate config file creation by setting and
    getting it's class variables."""

    access_key = ""
    secret_key = ""
    user_url = "s3-stage.biznetgio.net"
    admin_url = "103.77.104.76"
    admin_port = "19443"
    admin_username = ""
    admin_password = ""

    def dump_config(self, options, cfg):
        cfg_file = config_file()
        config = ""
        for option in options:
            value = getattr(cfg, option[0])

            option = f"OS_{option[0].upper()}"
            config += f"{option}={value}\n"
        try:
            with io.open(cfg_file, "w") as fp:
                fp.write(config)
                click.secho(f"\nConfiguration saved to {cfg_file}", fg="green")
        except IOError as e:
            click.secho(
                f"\nWriting config file failed: {cfg_file}: {e.strerror}",
                fg="yellow",
                bold=True,
                err=True,
            )
            sys.exit()


def config_file():
    home = os.path.expanduser("~")
    cfg_file = os.path.join(home, ".config", "neo-obs", "obs.env")
    return cfg_file


def is_config_exists():
    cfg_file = config_file()
    return os.path.isfile(cfg_file)


def load_config_file():
    # load_dotenv didn't have it's own exception
    if is_config_exists():
        cfg_file = config_file()
        dotenv.load_dotenv(cfg_file, override=True)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cfg_file)