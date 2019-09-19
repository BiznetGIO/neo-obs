import tabulate
import click

from obs.libs import user as user_lib
from obs.admin import user_profile
from obs.libs import utils


def list_user(client, group_id, user_type, user_status, limit):
    users = user_lib.list_user(
        client=client, group_id=group_id, user_type=user_type, user_status=user_status
    )
    utils.check(users)
    number = 1  # must start from 1 (as user data)
    results = []
    if not limit:
        limit = len(users)
    for _, user in zip(range(limit), users):
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


def info(client, user_id, group_id):
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


def create(client):
    data = user_profile.prompt_user_profile()
    response = user_lib.create(client, data)
    utils.check(response)
    click.secho(f"User created successfully", fg="green")


def remove(client, user_id, group_id):
    response = user_lib.remove(client, user_id=user_id, group_id=group_id)

    utils.check(response)
    click.secho(f"User removed successfully", fg="green")
