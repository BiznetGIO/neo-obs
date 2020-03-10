import pytest
import mock

from obs.libs import user
from obs.libs import credential
from obs.libs import qos
from obs.libs import admin
from obs.api.app.controllers.api import admin as admin_client


def fake_client():
    client = mock.Mock()
    client.user.return_value = ""
    client.qos.limits.return_value = ""
    client.user.credentials.return_value = ""
    client.user.credentials.status.return_value = ""

    return client


def fake_list_users(client, group_id, user_type="all", user_status="active", limit=""):
    user1 = {
        "userId": "jerrygarcia",
        "fullName": "Jerry Garcia",
        "emailAddr": "garcia@bgn.net",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "active": "true",
        "canonicalUserId": "123",
    }
    user2 = {
        "userId": "johnthompson",
        "fullName": "John Thompson",
        "emailAddr": "",
        "address1": "",
        "city": "",
        "active": "true",
        "canonicalUserId": "123",
    }
    return [user1, user2]


def test_list(client, monkeypatch):
    monkeypatch.setattr(user, "list_user", fake_list_users)

    result = client.get("/api/admin/user", data={"groupId": "test"})
    assert result.get_json()["data"] == [
        {
            "userId": "jerrygarcia",
            "fullName": "Jerry Garcia",
            "emailAddr": "garcia@bgn.net",
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "active": "true",
            "canonicalUserId": "123",
        },
        {
            "userId": "johnthompson",
            "fullName": "John Thompson",
            "emailAddr": "",
            "address1": "",
            "city": "",
            "active": "true",
            "canonicalUserId": "123",
        },
    ]


def fake_qos_info(client, user_id, group_id):
    qos = {
        "groupId": "testing",
        "userId": "foo",
        "labelId": "foobar",
        "qosLimitList": [
            {"type": "STORAGE_QUOTA_KBYTES", "value": -1},
            {"type": "REQUEST_RATE_LW", "value": -1},
            {"type": "REQUEST_RATE_LH", "value": -1},
            {"type": "DATAKBYTES_IN_LW", "value": -1},
            {"type": "DATAKBYTES_IN_LH", "value": -1},
            {"type": "DATAKBYTES_OUT_LW", "value": -1},
            {"type": "DATAKBYTES_OUT_LH", "value": -1},
            {"type": "STORAGE_QUOTA_COUNT", "value": -1},
        ],
        "Storage Limit": "unlimited",
    }
    return qos


def test_qos_info(client, monkeypatch):
    monkeypatch.setattr(qos, "info", fake_qos_info)

    result = client.get("/api/admin/qos", data={"groupId": "test", "userId": "foo"})
    assert "unlimited" in result.get_json()["data"].values()


def fake_cred_list(client, user_id, group_id):
    cred = [{"accessKey": "123", "secretKey": "abc", "createDate": 000, "active": True}]
    return cred


def test_cred_list(client, monkeypatch):
    monkeypatch.setattr(credential, "list", fake_cred_list)

    result = client.get("/api/admin/cred", data={"groupId": "test", "userId": "foo"})
    assert result.get_json()["data"] == [
        {"accessKey": "123", "secretKey": "abc", "createDate": 000, "active": True}
    ]


def test_delete_user(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.delete("/api/admin/user", data={"groupId": "test", "userId": "foo"})
    assert result.get_json()["message"] == f"User foo deleted successfully."


def test_create_user(client, monkeypatch):
    pass


def test_set_qos(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.post(
        "/api/admin/qos", data={"groupId": "test", "userId": "foo", "limit": 100}
    )
    assert result.get_json()["message"] == f"User foo quota changed successfully."


def fake_usage():
    client_user = mock.Mock()
    client_user.usage.return_value = [
        {
            "groupId": "test",
            "userId": "foo",
            "region": "stage",
            "operation": "SB",
            "uri": "",
            "timestamp": "0",
            "value": "100",
            "count": "0",
            "whitelistValue": "0",
            "whitelistCount": "0",
            "maxValue": "0",
            "whitelistMaxValue": "0",
            "ip": "",
            "bucket": None,
            "policyId": None,
            "averageValue": "100",
            "whitelistAverageValue": "0",
        }
    ]
    return client_user


def test_usage(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_usage)

    result = client.get("/api/admin/usage", data={"groupId": "test", "userId": "foo"})
    assert "100" in result.get_json()["data"].values()


def test_create_cred(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.post("/api/admin/cred", data={"groupId": "test", "userId": "foo"})
    assert (
        result.get_json()["message"] == f"User foo new credential created successfully."
    )


def test_remove_cred(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.delete("/api/admin/cred", data={"access_key": "123"})
    assert result.get_json()["message"] == f"Access key 123 deleted successfully."


def test_status_cred(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.put("/api/admin/cred", data={"access_key": "123", "status": "true"})
    assert result.get_json()["message"] == f"Credential status has been activated."


def fake_user_info(client, group_id, user_id):
    user = {
        "userId": "jerrygarcia",
        "fullName": "Jerry Garcia",
        "emailAddr": "garcia@bgn.net",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "active": "true",
        "canonicalUserId": "123",
    }
    return user


def test_suspend_user(client, monkeypatch):
    monkeypatch.setattr(user, "info", fake_user_info)
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.put(
        "/api/admin/user", data={"groupId": "test", "userId": "foo", "suspend": "true"}
    )
    assert result.status_code == 200
    assert result.get_json()["message"] == "User has been suspended"


def test_create_user(client, monkeypatch):
    monkeypatch.setattr(admin_client, "get_client", fake_client)

    result = client.post(
        "/api/admin/user",
        data={
            "groupId": "test",
            "userId": "foo",
            "fullName": "foobar",
            "quotaLimit": 1000,
        },
    )
    assert result.get_json()["message"] == f"User foo created successfully."
