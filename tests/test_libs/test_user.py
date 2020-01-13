import mock
from obs.libs import user


def test_dump():
    usr = user.UserProfile
    options = [
        ("userId", "User ID"),
        ("groupId", "Group ID"),
        ("userType", "User Type"),
        ("fullName", "Full Name"),
        ("emailAddr", "Email"),
        ("address1", "Address"),
        ("city", "City"),
        ("state", "State"),
        ("zip", "Zip"),
        ("country", "Country"),
        ("phone", "Phone"),
        ("website", "Website"),
        ("active", "Active"),
        ("ldapEnabled", "LDAP Enabled"),
    ]

    assert user.UserProfile().dump(options, usr) == {
        "userId": "",
        "groupId": "",
        "userType": "User",
        "fullName": "",
        "emailAddr": "",
        "address1": "",
        "city": "",
        "state": "",
        "zip": "",
        "country": "",
        "phone": "",
        "website": "",
        "active": True,
        "ldapEnabled": False,
    }


def fake_list():
    user1 = {
        "userId": "jerrygarcia",
        "fullName": "Jerry Garcia",
        "emailAddr": "garcia@bgn.net",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "active": True,
    }
    user2 = {
        "userId": "johnthompson",
        "fullName": "John Thompson",
        "emailAddr": "",
        "address1": "",
        "city": "",
        "active": True,
    }

    ls = mock.Mock()
    ls.user.list.return_value = [user1, user2]
    return ls


def test_list():
    assert user.list_user(fake_list(), "group") == [
        {
            "userId": "jerrygarcia",
            "fullName": "Jerry Garcia",
            "emailAddr": "garcia@bgn.net",
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "active": True,
        },
        {
            "userId": "johnthompson",
            "fullName": "John Thompson",
            "emailAddr": "",
            "address1": "",
            "city": "",
            "active": True,
        },
    ]


def fake_info():
    user = {
        "userId": "johnthompson",
        "fullName": "John Thompson",
        "emailAddr": "jgarc@geemail.com",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "groupId": "testing",
        "canonicalUserId": "2c82bdc930155e8dc6860bfake",
        "active": True,
    }
    info = mock.Mock()
    info.user.return_value = user
    return info


def test_info():
    assert user.info(fake_info(), "ocean", "nature") == {
        "userId": "johnthompson",
        "fullName": "John Thompson",
        "emailAddr": "jgarc@geemail.com",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "groupId": "testing",
        "canonicalUserId": "2c82bdc930155e8dc6860bfake",
        "active": True,
    }


def fake_client():
    client = mock.Mock()
    client.user.return_value = "Done"
    return client


def test_create():
    assert user.create(fake_client(), "data") == "Done"


def test_remove():
    assert user.remove(fake_client(), "user", "group")
