import click
from functools import partial

from obs.libs import auth
from obs.admin import user as user_cli

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
    user_cli.user_info(client=client, user_id=user_id, group_id=group_id)


@user.command("create")
def create():
    """Create user."""
    client = get_admin_client()
    user_cli.create_user(client)
