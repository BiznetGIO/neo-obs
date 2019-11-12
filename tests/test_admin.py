import pytest
import io
import os
import mock
import obs.libs.auth
import obs.libs.user
import obs.libs.utils
import obs.admin.commands as admin_client

from datetime import datetime
from click.testing import CliRunner
from obs.main import cli
from pathlib import Path


def fake_client():
    pass


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(obs.libs.auth, "admin_client", fake_client)


def test_get_client(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "ls", "--user-id", "StageTest", "--group-id", "testing"]
    )
    path = str(Path.home()) + "/.config/neo-obs/obs.env"
    assert result.output == (
        f"[Errno 2] No such file or directory: '{path}'\n"
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one\n"
    )


def fake_list_users(client, group_id, user_type="all", user_status="active", limit=""):
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
    return [user1, user2]


def test_ls(monkeypatch, client):
    monkeypatch.setattr(obs.libs.user, "list_user", fake_list_users)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "admin",
            "user",
            "ls",
            "--group-id",
            "testing",
            "--user-type",
            "all",
            "--user-status",
            "active",
        ],
    )

    fixture_path = os.path.join("tests", "fixture", "tabulated_users")
    with io.open(fixture_path, "rt", encoding="utf8") as f:
        tabulated_users = f.read()

    assert result.output == tabulated_users


def test_except_ls(client):
    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "user", "ls"])

    assert result.output == (
        f"Users fetching failed. \n" f"'NoneType' object has no attribute 'user'\n"
    )


def fake_info(client, user_id, group_id):
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
    return user


def test_info(monkeypatch, client):
    monkeypatch.setattr(obs.libs.user, "info", fake_info)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["admin", "user", "info", "--user-id", "StageTest", "--group-id", "testing"],
    )

    assert result.output == (
        f"ID: johnthompson\n"
        f"Name: John Thompson\n"
        f"Email: jgarc@geemail.com\n"
        f"Address: 456 Shakedown St.\n"
        f"City: Portsmouth\n"
        f"Group ID: testing\n"
        f"Canonical ID: 2c82bdc930155e8dc6860bfake\n"
        f"Active: True\n"
    )


def test_except_info(client):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["admin", "user", "info", "--user-id", "StageTest", "--group-id", "testing"],
    )

    assert result.output == (
        f"User info fetching failed. \n" f"'NoneType' object has no attribute 'user'\n"
    )


def fake_qos_info(client, user_id, group_id):
    limits = [
        {"type": "STORAGE_QUOTA_KBYTES", "value": -1},
        {"type": "REQUEST_RATE_LW", "value": -1},
        {"type": "REQUEST_RATE_LH", "value": -1},
        {"type": "DATAKBYTES_IN_LW", "value": -1},
        {"type": "DATAKBYTES_IN_LH", "value": -1},
        {"type": "DATAKBYTES_OUT_LW", "value": -1},
        {"type": "DATAKBYTES_OUT_LH", "value": -1},
        {"type": "STORAGE_QUOTA_COUNT", "value": -1},
    ]
    qos = {"groupId": "testing", "userId": "johnthompson", "qosLimitList": limits}
    return qos


def test_qos_info(monkeypatch, client):
    monkeypatch.setattr(obs.libs.qos, "info", fake_qos_info)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "info", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Group ID: testing\n" f"User ID: johnthompson\n" f"Storage Limit: Unlimited\n"
    )


def test_except_qos_info(client):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "info", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Storage limit fetching failed. \n"
        f"'NoneType' object has no attribute 'qos'\n"
    )


def fake_cred_list(client, user_id, group_id):
    dt = datetime(2019, 9, 24, 13, 18, 7, 0).timestamp()
    credential = {
        "accessKey": "394b287c9efake",
        "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
        "createDate": dt,
        "active": True,
    }
    return [credential]


def fake_human_date(unixtime):
    return "1970-01-19 10:55:05+0700 (WIB)"


def test_cred_list(monkeypatch, client):
    monkeypatch.setattr(obs.libs.credential, "list", fake_cred_list)
    monkeypatch.setattr(obs.libs.utils, "human_date", fake_human_date)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "ls", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Access Key: 394b287c9efake\n"
        f"Secret Key: IgP23gfnbrguu21YqFRw4+7Mfake\n"
        f"Created: 1970-01-19 10:55:05+0700 (WIB)\n"
        f"Active: True\n"
    )


def test_except_cred_list(client):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "ls", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Credentials listing failed. \n" f"'NoneType' object has no attribute 'user'\n"
    )


def fake_clients():
    user = [
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
    client = mock.Mock()
    client.user.list.return_value = user
    client.user.side_effect = client.user.list().pop(1)
    return client


def test_remove_user(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_clients)
    monkeypatch.setattr(obs.libs.utils, "check", lambda response: None)

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "user", "rm"])

    assert fake_clients().user.list() == [
        {
            "userId": "jerrygarcia",
            "fullName": "Jerry Garcia",
            "emailAddr": "garcia@bgn.net",
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "active": True,
        }
    ]


def test_except_remove_user(client):
    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "user", "rm"])
    assert result.output == (
        f"User removal failed. \n" f"'NoneType' object has no attribute 'user'\n"
    )


def fake_creds():
    credential = [
        {
            "accessKey": "394b287c9efake",
            "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
            "createDate": "1970-01-19 10:55:05+0700 (WIB)",
            "active": True,
        },
        {
            "accessKey": "Br432sd293fake",
            "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
            "createDate": "2019-01-19 10:55:05+0700 (WIB)",
            "active": True,
        },
    ]
    cred = mock.Mock()
    cred.user.credentials.list.return_value = credential

    def remove():
        del cred.user.credentials.list()[1]

    cred.user.credentials.side_effect = remove()
    return cred


def test_remove_cred(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_creds)
    monkeypatch.setattr(obs.libs.utils, "check", lambda cred: None)

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "cred", "rm"])

    assert fake_creds().user.credentials.list() == [
        {
            "accessKey": "394b287c9efake",
            "secretKey": "IgP23gfnbrguu21YqFRw4+7Mfake",
            "createDate": "1970-01-19 10:55:05+0700 (WIB)",
            "active": True,
        }
    ]


def test_except_remove_cred(client):
    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "cred", "rm"])

    assert result.output == (
        f"Credential removal failed. \n" f"'NoneType' object has no attribute 'user'\n"
    )
