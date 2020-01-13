import pytest
import io
import os
import mock
import bitmath
from datetime import datetime

import obs.libs.auth
import obs.libs.user
import obs.libs.utils
import obs.admin.commands as admin_client
from click.testing import CliRunner
from obs.main import cli


def fake_client():
    pass


def fake_response():
    return {"reason": "error", "status_code": 101, "url": "http://testing"}


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(obs.libs.auth, "admin_client", fake_client)


def test_get_client(monkeypatch):
    monkeypatch.setattr(obs.libs.config, "config_file", lambda: "home/user/path")

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "user", "ls"])
    assert result.output == (
        f"[Errno 2] No such file or directory: 'home/user/path'\n"
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one\n"
    )


def fake_exc_client():
    client = mock.Mock()
    client.user.list.return_value = fake_response()
    client.user.return_value = fake_response()
    client.qos.limits.return_value = fake_response()
    client.user.credentials.list.return_value = fake_response()

    return client


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


def test_except_ls(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "user", "ls"])

    assert result.output == (
        f"Users fetching failed. \n" f"error [101]\n" f"URL: http://testing\n"
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


def test_except_info(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["admin", "user", "info", "--user-id", "StageTest", "--group-id", "testing"],
    )

    assert result.output == (
        f"User info fetching failed. \n" f"error [101]\n" f"URL: http://testing\n"
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
    monkeypatch.setattr(bitmath, "kB", fake_bitmath)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "info", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Group ID: testing\n" f"User ID: johnthompson\n" f"Storage Limit: Unlimited\n"
    )


def fake_bitmath(limit):
    limit = mock.Mock()
    limit.to_GiB.return_value.best_prefix.return_value = "0.49234 GiB"
    return limit


def test_except_qos_info(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "info", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Storage limit fetching failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )


def fake_qos():
    client = mock.Mock()
    client.qos.limits.return_value = "Done"
    return client


def test_qos_set(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_qos)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "admin",
            "qos",
            "set",
            "--user-id",
            "user",
            "--group-id",
            "group",
            "--limit",
            100,
        ],
    )

    assert result.output == f"Storage limit changed\n"


def test_except_qos_set(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "admin",
            "qos",
            "set",
            "--user-id",
            "user",
            "--group-id",
            "group",
            "--limit",
            100,
        ],
    )

    assert (
        result.output == f"Storage limit change failed. \n"
        f"error [101]\n"
        f"URL: http://testing\n"
    )


def test_qos_rm(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_qos)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "rm", "--user-id", "user", "--group-id", "group"]
    )

    assert result.output == f"Storage limit removed\n"


def test_except_qos_rm(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "qos", "rm", "--user-id", "user", "--group-id", "group"]
    )

    assert (
        result.output == f"Storage limit removal failed. \n"
        f"error [101]\n"
        f"URL: http://testing\n"
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


def test_except_cred_list(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_exc_client)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "ls", "--user-id", "StageTest", "--group-id", "testing"]
    )

    assert result.output == (
        f"Credentials listing failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )


def fake_user():
    client = mock.Mock()
    client.user.return_value = fake_response()
    return client


def test_remove_user(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_user)
    monkeypatch.setattr(obs.libs.utils, "check", lambda response: None)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "user", "rm", "--user-id", "user", "--group-id", "group"]
    )

    assert result.output == f"User removed successfully\n"


def test_except_remove_user(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_user)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "user", "rm", "--user-id", "user", "--group-id", "group"]
    )
    assert result.output == (
        f"User removal failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )


def fake_rm_creds():
    cred = mock.Mock()
    cred.user.credentials.return_value = fake_response()
    return cred


def test_remove_cred(monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_rm_creds)
    monkeypatch.setattr(obs.libs.utils, "check", lambda cred: None)

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "cred", "rm", "--access-key", "foo"])

    assert result.output == f"Credentials removed\n"


def test_except_remove_cred(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_admin_client", fake_rm_creds)

    runner = CliRunner()
    result = runner.invoke(cli, ["admin", "cred", "rm", "--access-key", "foo"])

    assert result.output == (
        f"Credential removal failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )


def fake_status_creds():
    client = mock.Mock()
    client.user.credentials.status.return_value = fake_response()
    return client


def test_status_cred(monkeypatch):
    monkeypatch.setattr(obs.admin.commands, "get_admin_client", fake_status_creds)
    monkeypatch.setattr(obs.libs.utils, "check", lambda cred: None)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "status", "--access-key", "Br432sd293fake"]
    )

    assert result.output == f"Credentials status changed\n"


def test_except_status_cred(client, monkeypatch):
    monkeypatch.setattr(obs.admin.commands, "get_admin_client", fake_status_creds)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "status", "--access-key", "Br432sd293fake"]
    )
    assert result.output == (
        f"Credentials fetching failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )


def fake_create_creds():
    client = mock.Mock()
    client.user.credentials.return_value = fake_response()
    return client


def test_create_cred(monkeypatch):
    monkeypatch.setattr(obs.admin.commands, "get_admin_client", fake_create_creds)
    monkeypatch.setattr(obs.libs.utils, "check", lambda cred: None)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "create", "--user-id", "user", "--group-id", "group"]
    )

    assert result.output == f"Credentials created\n"


def test_except_create_cred(client, monkeypatch):
    monkeypatch.setattr(obs.admin.commands, "get_admin_client", fake_create_creds)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["admin", "cred", "create", "--user-id", "user", "--group-id", "group"]
    )
    assert result.output == (
        f"Credential creation failed. \n" f"error [101]\n" f"URL: http://testing\n"
    )
