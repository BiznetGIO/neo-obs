def list(client, user_id, group_id):
    """Get security credentials of  user."""
    credentials = client.user.credentials.list(
        method="GET", userId=user_id, groupId=group_id
    )
    return credentials


def status(client, access_key, status=True):
    """Set security credentials status."""
    status = client.user.credentials.status(
        method="POST", accessKey=access_key, isActive=status
    )
    return status


def rm(client, access_key):
    """Remove security credentials."""
    credentials = client.user.credentials(method="DELETE", accessKey=access_key)
    return credentials


def create(client, user_id, group_id):
    """Create security credentials."""
    credentials = client.user.credentials(
        method="PUT", userId=user_id, groupId=group_id
    )
    return credentials
