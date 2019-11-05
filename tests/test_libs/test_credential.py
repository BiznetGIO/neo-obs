import mock, pytest
from obs.libs import credential as cred


def fake_client():
    client = mock.Mock()
    client.user.credentials.list.return_value = {
        "accessKey": "394b287c9efake",
        "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
        "createDate": "1970-01-19 10:55:05+0700 (WIB)",
        "active": True,
    }
    client.user.credentials.status.return_value = "Done"
    client.user.credentials.return_value = "Done"
    return client


def test_list():
    assert cred.list(fake_client(), "user", "group") == {
        "accessKey": "394b287c9efake",
        "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
        "createDate": "1970-01-19 10:55:05+0700 (WIB)",
        "active": True,
    }


def test_status():
    assert cred.status(fake_client(), "key") == "Done"


def test_rm():
    assert cred.rm(fake_client(), "key") == "Done"


def test_create():
    assert cred.create(fake_client(), "user", "group") == "Done"
