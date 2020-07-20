import click

from obs.libs import config


def run_configure():
    """Prompt user interactively for config values and write those values to config_file."""
    cfg = config.Config()
    options = [
        (
            "user_access_key",
            "Access Key",
            "Access key and Secret key are your identifiers for object storage service",
        ),
        ("user_secret_key", "Secret Key"),
        (
            "user_url",
            "Object Storage Endpoint",
            f'Use "{cfg.user_url}" for Neo Object Storage.',
        ),
        (
            "user_gmt_policy",
            "Gmt Policy Path",
            f"Path to your gmt policy file, Leave as is 'notset' if you don't want to use Cloudian extension",
        ),
        (
            "admin_username",
            "Admin Username",
            f"""Admin username and password are your identifiers for your admin panel.""",
        ),
        ("admin_password", "Admin Password"),
        (
            "admin_url",
            "Admin URL",
            f"Admin url and port are your url and port location to your admin panel.",
        ),
        ("admin_port", "Admin port"),
        (
            "use_https",
            "Use HTTPS protocol",
            "All communication is protected when enabled, but it's slower than plain HTTP.",
        ),
        (
            "use_neo",
            "Use NEO compatibility",
            "Use NEO compatibility for adding specific policy id in Object Storage.",
        ),
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
