import pytest
from click.testing import CliRunner
import io
import os
from datetime import datetime

from obs.main import cli
import obs.libs.auth
import obs.libs.user
import obs.libs.utils


def fake_client():
    pass


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(obs.libs.auth, "admin_client", fake_client)


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
