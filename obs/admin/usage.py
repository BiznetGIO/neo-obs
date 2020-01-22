import click
import bitmath

from obs.libs import admin as admin_lib
from obs.libs import utils


def du(client, user_id, group_id):
    try:
        usage = admin_lib.usage(client, user_id, group_id)
        utils.check(usage)
        value = usage[0]["value"]
        prefixed_value = bitmath.Byte(int(value)).best_prefix()
        click.secho(f"Storage usage: {prefixed_value}")
    except Exception as exc:
        click.secho(
            f"Storage fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )
