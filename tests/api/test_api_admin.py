import pytest
import mock

from obs.libs import user
from obs.libs import credential
from obs.libs import qos


def fake_list_users(client, group_id, user_type="all", user_status="active", limit=""):
    user1 = {
        "userId": "jerrygarcia",
        "fullName": "Jerry Garcia",
        "emailAddr": "garcia@bgn.net",
        "address1": "456 Shakedown St.",
        "city": "Portsmouth",
        "active": "true",
    }
    user2 = {
        "userId": "johnthompson",
        "fullName": "John Thompson",
        "emailAddr": "",
        "address1": "",
        "city": "",
        "active": "true",
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
        },
        {
            "userId": "johnthompson",
            "fullName": "John Thompson",
            "emailAddr": "",
            "address1": "",
            "city": "",
            "active": "true",
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
