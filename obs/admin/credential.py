import click

from obs.libs import credential as cred_lib
from obs.libs import utils


def list(client, user_id, group_id):
    credentials = cred_lib.list(client, user_id, group_id)
    utils.check(credentials)
    credential = credentials[0]
    human_date = utils.human_date(credential["createDate"])
    result = (
        f"Access Key: {credential['accessKey']}\n"
        f"Secret Key: {credential['secretKey']}\n"
        f"Created: {human_date}\n"
        f"Active: {credential['active']}"
    )
    click.secho(result)


def status(client, access_key, status):
    status = cred_lib.status(client, access_key, status)
    utils.check(status)
    click.secho(f"Credentials status changed", fg="green")


def rm(client, access_key):
    credentials = cred_lib.rm(client, access_key)
    utils.check(credentials)
    click.secho(f"Credentials removed", fg="green")


def create(client, user_id, group_id):
    credentials = cred_lib.create(client, user_id, group_id)
    utils.check(credentials)
    click.secho(f"Credentials created", fg="green")
