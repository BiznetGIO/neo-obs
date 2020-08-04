import tabulate
import click

from obs.libs import user as user_lib
from obs.cli.admin import user_profile
from obs.libs import utils


def list_user(client, group_id, user_type, user_status, limit):
    try:
        users = user_lib.list_user(
            client=client,
            group_id=group_id,
            user_type=user_type,
            user_status=user_status,
            limit=limit,
        )
        utils.check(users)
        number = 1  # must start from 1 (as user data)
        results = []
        for user in users:
            data = {
                "No": number,
                "User": user["userId"],
                "Name": user["fullName"],
                "Email": user["emailAddr"],
                "Address": user["address1"],
                "City": user["city"],
                "Status": user["active"],
            }
            number += 1
            results.append(data)
        click.secho(tabulate.tabulate(results, headers="keys", tablefmt="grid"))
    except Exception as exc:
        click.secho(f"Users fetching failed. \n{exc}", fg="yellow", bold=True, err=True)


def info(client, user_id, group_id):
    try:
        user = user_lib.info(client=client, user_id=user_id, group_id=group_id)
        utils.check(user)
        result = (
            f"ID: {user['userId']}\n"
            f"Name: {user['fullName']}\n"
            f"Email: {user['emailAddr']}\n"
            f"Address: {user['address1']}\n"
            f"City: {user['city']}\n"
            f"Group ID: {user['groupId']}\n"
            f"Canonical ID: {user['canonicalUserId']}\n"
            f"Active: {user['active']}"
        )
        click.secho(result)
    except Exception as exc:
        click.secho(
            f"User info fetching failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def create(client):
    try:
        data = user_profile.prompt_user_profile()
        response = user_lib.create(client, data)
        utils.check(response)
        click.secho(f"User created successfully", fg="green")
    except Exception as exc:
        click.secho(f"User creation failed. \n{exc}", fg="yellow", bold=True, err=True)


def suspend(client, user_id, group_id, status):
    try:
        user_info = user_lib.info(client=client, user_id=user_id, group_id=group_id)
        message = "suspended" if status is True else "unsuspended"
        data = {key: val for key, val in user_info.items() if "canonical" not in key}
        data["active"] = not status
        response = user_lib.update(client, data)
        utils.check(response)
        click.secho(f"User {message} successfully", fg="green")
    except Exception as exc:
        click.secho(
            f"User suspension failed. \n{exc}", fg="yellow", bold=True, err=True
        )


def remove(client, user_id, group_id):
    try:
        response = user_lib.remove(client=client, user_id=user_id, group_id=group_id)
        utils.check(response)
        click.secho(f"User removed successfully", fg="green")
    except Exception as exc:
        click.secho(f"User removal failed. \n{exc}", fg="yellow", bold=True, err=True)
