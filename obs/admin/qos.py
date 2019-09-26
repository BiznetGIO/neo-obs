import click
import bitmath

from obs.libs import qos as qos_lib
from obs.libs import utils


def get_limit_kbytes(qos):
    """Get kilobytes limit of storage in QoS response."""
    qos_limits = qos["qosLimitList"]
    limit = 0
    for item in qos_limits:
        if item["type"] == "STORAGE_QUOTA_KBYTES":
            limit = item["value"]
            break

    if limit == -1:
        limit = "Unlimited"
    else:
        limit = bitmath.kB(limit).to_GiB().best_prefix()

    return limit


def info(client, user_id, group_id):
    try:
        qos = qos_lib.info(client, user_id=user_id, group_id=group_id)
        utils.check(qos)
        qos_limit = get_limit_kbytes(qos)
        msg = (
            f"Group ID: {qos['groupId']}\n"
            f"User ID: {qos['userId']}\n"
            f"Storage Limit: {qos_limit}"
        )
        click.secho(msg)
    except Exception as exc:
        click.secho(
            f"Storage limit fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def set(client, user_id, group_id, limit):
    try:
        qos = qos_lib.set(client, user_id=user_id, group_id=group_id, limit=limit)
        utils.check(qos)
        click.secho("Storage limit changed", fg="green")
    except Exception as exc:
        click.secho(
            f"Storage limit set failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def rm(client, user_id, group_id):
    try:
        qos = qos_lib.rm(client, user_id=user_id, group_id=group_id)
        utils.check(qos)
        click.secho("Storage limit removed", fg="green")
    except Exception as exc:
        click.secho(
            f"Storage limit removal failed. \n{exc}", fg="yellow", bold=True, err=True
        )
