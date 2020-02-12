import click

from obs.libs import credential as cred_lib
from obs.libs import utils


def list(client, user_id, group_id):
    try:
        credentials = cred_lib.list(client, user_id, group_id)
        utils.check(credentials)
        for credential in credentials:
            human_date = utils.human_date(credential["createDate"])
            result = (
                f"Access Key: {credential['accessKey']}\n"
                f"Secret Key: {credential['secretKey']}\n"
                f"Created: {human_date}\n"
                f"Active: {credential['active']}"
            )
            click.secho(result)
    except Exception as exc:
        click.secho(
            f"Credentials listing failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def status(client, access_key, status):
    try:
        status = cred_lib.status(client, access_key, status)
        utils.check(status)
        click.secho(f"Credentials status changed", fg="green")
    except Exception as exc:
        click.secho(
            f"Credentials fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def rm(client, access_key):
    try:
        credentials = cred_lib.rm(client, access_key)
        utils.check(credentials)
        click.secho(f"Credentials removed", fg="green")
    except Exception as exc:
        click.secho(
            f"Credential removal failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def create(client, user_id, group_id):
    try:
        credentials = cred_lib.create(client, user_id, group_id)
        utils.check(credentials)
        click.secho(f"Credentials created", fg="green")
    except Exception as exc:
        click.secho(
            f"Credential creation failed. \n{exc}", fg="yellow", bold=True, err=True
        )
