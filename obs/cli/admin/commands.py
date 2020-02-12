import click
import sys
from functools import partial

from obs.libs import auth
from obs.cli.admin import user as user_cli
from obs.cli.admin import qos as qos_cli
from obs.cli.admin import credential as cred_cli
from obs.cli.admin import usage as usage_cli
from obs.libs import config

click.option = partial(click.option, show_default=True)


def get_admin_client():
    try:
        config.load_config_file()
        admin_client = auth.admin_client()
        return admin_client
    except Exception as exc:
        click.secho(str(exc), fg="yellow", bold=True, err=True)
        msg = (
            f"Configuration file not available.\n"
            f"Consider running 'obs --configure' to create one"
        )
        click.secho(msg, fg="yellow", bold=True, err=True)
        sys.exit(1)


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
@click.option("--limit", "limit", default="", help="Maximum data length")
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


@admin.group()
def cred():
    """administrate user credentials."""


@cred.command("ls")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def ls(user_id, group_id):
    """Show user's credentials."""
    client = get_admin_client()
    cred_cli.list(client, user_id, group_id)


@cred.command("status")
@click.option("--access-key", "access_key", type=str, help="User Access Key")
@click.option("--status", "status", default=True, help="Set Status")
def status(access_key, status):
    """Set user's credentials status."""
    client = get_admin_client()
    cred_cli.status(client, access_key, status)


@cred.command("rm")
@click.option("--access-key", "access_key", type=str, help="User Access Key")
def rm(access_key):
    """Remove user's credentials."""
    client = get_admin_client()
    cred_cli.rm(client, access_key)


@cred.command("create")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def create(user_id, group_id):
    """Create user's credentials."""
    client = get_admin_client()
    cred_cli.create(client, user_id, group_id)


@admin.group()
def usage():
    """Administrate usage."""


@usage.command("du")
@click.option("--user-id", "user_id", type=str, help="User ID")
@click.option("--group-id", "group_id", type=str, help="Group ID")
def du(user_id, group_id):
    """Show user's usage."""
    client = get_admin_client()
    usage_cli.du(client, user_id, group_id)
