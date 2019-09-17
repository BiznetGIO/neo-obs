import tabulate
import click

from obs.libs import user as user_lib


def list_user(client, group_id, user_type, user_status, limit):
    users = user_lib.list_user(
        client=client, group_id=group_id, user_type=user_type, user_status=user_status
    )
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
