class UserData:
    """Accommodate user data creation by setting and
    getting it's class variables."""

    active = True
    ldapEnabled = False
    userId = ""
    groupId = ""
    userType = "User"
    fullName = ""
    emailAddr = ""
    address1 = ""
    address2 = ""
    city = ""
    state = ""
    zip = ""
    country = ""
    phone = ""
    website = ""

    def dump_data(self, options, cfg):
        data = {}
        for option in options:
            value = getattr(cfg, option[0])
            data[option[0]] = value
        return data


def list_user(client, group_id, user_type="all", user_status="active"):
    """Get all user info."""
    users = client.user.list(
        groupId=group_id, userType=user_type, userStatus=user_status
    )
    return users


def user_info(client, user_id, group_id):
    """Get user info"""
    user = client.user(userId=user_id, groupId=group_id)
    return user


def create_user(client, data):
    """Create user"""
    client.user(method="PUT", json=data)


def remove_user(client, user_id, group_id):
    """Remove user"""
    client.user(method="DELETE", userId=user_id, groupId=group_id)
