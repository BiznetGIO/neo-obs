import click

from obs.libs import gmt


def show_policies():
    policies = gmt.get_policies()
    try:
        for zone in policies:
            policy_id, description, _ = policies[zone].values()
            if not description:
                description = "No description"
            msg = f"Name: {zone}\n" f"Id: {policy_id}\n" f"Description: {description}\n"
            click.secho(msg)
    except Exception as exc:
        click.secho(f"Show policies failed. \n{exc}", fg="yellow", bold=True, err=True)
