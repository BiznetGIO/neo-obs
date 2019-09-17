def list_user(client, group_id, user_type="all", user_status="active"):
    """Get all user info."""
    users = client.user.list(
        groupId=group_id, userType=user_type, userStatus=user_status
    )
    return users
