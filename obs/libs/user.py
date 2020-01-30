class UserProfile:
    """Accommodate user profile creation by setting and
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

    def dump(self, options, cfg):
        """Dump user profile data"""
        data = {}
        for option in options:
            value = getattr(cfg, option[0])
            data[option[0]] = value
        return data


def list_user(client, group_id, user_type="all", user_status="active", limit=""):
    """List all users."""
    users = client.user.list(
        groupId=group_id, userType=user_type, userStatus=user_status, limit=limit
    )
    return users


def info(client, user_id, group_id):
    """Get user info"""
    user = client.user(userId=user_id, groupId=group_id)
    return user


def create(client, data):
    """Create user"""
    response = client.user(method="PUT", json=data)
    return response


def update(client, data):
    """Update user info"""
    response = client.user(method="POST", json=data)
    return response


def remove(client, user_id, group_id):
    """Remove user"""
    response = client.user(method="DELETE", userId=user_id, groupId=group_id)
    return response
