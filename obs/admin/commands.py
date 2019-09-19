import click
from functools import partial

from obs.libs import auth
from obs.admin import user as user_cli
from obs.admin import qos as qos_cli

click.option = partial(click.option, show_default=True)


def get_admin_client():
    try:
        admin_client = auth.admin_client()
        return admin_client
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)


@click.group()
def admin():
    """administrate object storage."""


@admin.group()
def user():
    """administrate user."""


@user.command("ls")
@click.option("--group-id", "group_id", type=str, help="Group ID")
@click.option("--user-type", "user_type", default="all", help="User Type")
@click.option("--user-status", "user_status", default="active", help="User Status")
@click.option("--limit", "limit", type=int, help="Maximum data length")
def list(group_id, user_type, user_status, limit):
    """List users."""
    client = get_admin_client()
    user_cli.list_user(
        client=client,
        group_id=group_id,
        user_type=user_type,
        user_status=user_status,
        limit=limit,
    )


@user.command("info")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def info(user_id, group_id):
    """Get user info."""
    client = get_admin_client()
    user_cli.info(client=client, user_id=user_id, group_id=group_id)


@user.command("create")
def create():
    """Create user."""
    client = get_admin_client()
    user_cli.create(client)


@user.command("rm")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def rm(user_id, group_id):
    """Remove user"""
    client = get_admin_client()
    user_cli.remove(client, user_id=user_id, group_id=group_id)


@admin.group()
def qos():
    """administrate QoS."""


@qos.command("info")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def info(user_id, group_id):
    """Get QoS info of specified user"""
    client = get_admin_client()
    qos_cli.info(client, user_id=user_id, group_id=group_id)


@qos.command("set")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
@click.option("--limit", "limit", type=int, help="Storage limit")
def set(user_id, group_id, limit):
    """Set QoS of specified user"""
    client = get_admin_client()
    qos_cli.set(client, user_id=user_id, group_id=group_id, limit=limit)


@qos.command("rm")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def rm(user_id, group_id):
    """Remove QoS of specified user"""
    client = get_admin_client()
    qos_cli.rm(client, user_id=user_id, group_id=group_id)
