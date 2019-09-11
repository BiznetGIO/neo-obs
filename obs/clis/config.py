import dotenv
import os
import errno
import click
import io


class Config:
    access_key = ""
    secret_key = ""
    user_url = "s3-stage.biznetgio.net"
    admin_url = "103.77.104.76"
    admin_port = "19443"
    admin_username = ""
    admin_password = ""

    def config_file(self):
        home = os.path.expanduser("~")
        config_file = os.path.join(home, ".config", "neo-obs", "neo.env")
        return config_file

    def is_config_exists(self):
        config_file = self.config_file()
        return os.path.isfile(config_file)

    def load_config_file(self):
        try:
            config_file = self.config_file()
            dotenv.load_dotenv(config_file)
        except:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), config_file
            )

    def dump_config(self, options, cfg):
        config_file = self.config_file()
        config = ""
        for option in options:
            value = getattr(cfg, option[0])

            option = f"OS_{option[0].upper()}"
            config += f"{option}={value}\n"
        try:
            with io.open(config_file, "w") as fp:
                fp.write(config)
            click.secho(f"\nConfiguration saved to {config_file}", fg="green")
        except IOError as e:
            click.secho(
                f"\nWriting config file failed: {config_file}: {e.strerror}",
                fg="yellow",
                bold=True,
                err=True,
            )
            sys.exit(EX_IOERR)


def run_configure():
    """Prompt user interactively for config values and write those values to config_file."""
    cfg = Config()
    options = [
        (
            "access_key",
            "Access Key",
            "Access key and Secret key are your identifiers for object storage service",
        ),
        ("secret_key", "Secret Key"),
        (
            "user_url",
            "Object Storage Endpoint",
            f'Use "{cfg.user_url}" for Neo Object Storage.',
        ),
        (
            "admin_username",
            "Admin Username",
            f"""Admin username and password are your identififers for your admin panel (e.g Clodian CMC), \nUse "{cfg.admin_url}" to the target Neo Object Storage.""",
        ),
        ("admin_password", "Admin Password"),
        (
            "admin_url",
            "Admin URL",
            f'Admin url and port are your url and port location to your admin panel Default "{cfg.admin_port}""',
        ),
        ("admin_port", "Admin port", f'Default "{cfg.admin_port}"'),
    ]
    try:
        while True:
            click.secho("Put in new values or accept defaults.")
            click.secho("See user manual for complete description of options.")
            for option in options:
                prompt = option[1]
                val = getattr(cfg, option[0])
                if val not in (None, ""):
                    prompt += f" [{val}]"

                if len(option) >= 3:
                    click.secho(f"\n{option[2]}")

                val = input(prompt + ": ")
                # only set new value if user provide one
                if val != "":
                    setattr(cfg, option[0], val)

            val = input("\nSave settings? [y/N] ")
            if val.lower().startswith("y"):
                break

            val = input("Retry configuration? [Y/n] ")
            if val.lower().startswith("n"):
                raise EOFError()

        cfg.dump_config(options, cfg)

    except (EOFError, KeyboardInterrupt):
        click.secho(
            "\nConfiguration aborted. Changes were NOT saved.",
            fg="yellow",
            bold=True,
            err=True,
        )
        return
