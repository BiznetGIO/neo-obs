import tabulate
import click
import sys

from obs.libs import user as user_lib
from obs.admin import user_data


def check_response(response):
    """Check if response contains error result
    then raise exception."""
    sys.tracebacklimit = 0

    if "reason" in response:
        msg = (
            f"{response.get('reason')} [{response.get('status_code')}]\n"
            f"URL: {response.get('url')}"
        )
        raise ValueError(msg)


def list_user(client, group_id, user_type, user_status, limit):
    users = user_lib.list_user(
        client=client, group_id=group_id, user_type=user_type, user_status=user_status
    )
    check_response(users)
    number = 1  # must start from 1 (as user data)
    results = []
    if not limit:
        limit = len(users)
    for _, user in zip(range(limit), users):
        data = {
            "No": number,
            "User": user["userId"],
            "Name": user["fullName"],
            "EmailAddr": user["emailAddr"],
            "Address": user["address1"],
            "City": user["city"],
            "Status": user["active"],
        }
        number += 1
        results.append(data)
    click.secho(tabulate.tabulate(results, headers="keys", tablefmt="grid"))


def user_info(client, user_id, group_id):
    user = user_lib.user_info(client=client, user_id=user_id, group_id=group_id)
    check_response(user)
    result = (
        f"ID: {user['userId']}\n"
        f"Name: {user['fullName']}\n"
        f"EmailAddr: {user['emailAddr']}\n"
        f"Address: {user['address1']}\n"
        f"City: {user['city']}\n"
        f"Group ID: {user['groupId']}\n"
        f"Canonical ID: {user['canonicalUserId']}\n"
        f"Active: {user['active']}"
    )
    click.secho(result)


def create_user(client):
    data = user_data.prompt_user_data()
    response = user_lib.create_user(client, data)
    check_response(response)
    click.secho(f"User created successfully", fg="green")


def remove_user(client, user_id, group_id):
    response = user_lib.remove_user(client, user_id=user_id, group_id=group_id)

    check_response(response)
    click.secho(f"User removed successfully", fg="green")
