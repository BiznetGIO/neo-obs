import click

from obs.libs import gmt


def show_policies():
    policies = gmt.get_policies()
    if policies == "notset":
        docs_url = "#using-cloudian-hyperstore-extension"
        msg = (
            f"Can't find Policy file\n"
            f"See '{docs_url}' in our documentation for more information"
        )
        click.secho(f"{msg}", fg="yellow", bold=True, err=True)
        return

    try:
        for zone in policies:
            policy_id, description, _ = policies[zone].values()
            if not description:
                description = "No description"
            msg = f"Name: {zone}\n" f"Id: {policy_id}\n" f"Description: {description}\n"
            click.secho(msg)
    except Exception as exc:
        click.secho(f"Show policies failed. \n{exc}", fg="yellow", bold=True, err=True)
