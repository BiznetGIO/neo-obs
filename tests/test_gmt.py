import os, mock, requests, yaml

import obs.libs.gmt as gmt
import obs.libs.auth as auth


def test_policies_file():
    assert gmt.policies_file() == (
        os.path.expanduser("~") + "/.config/neo-obs/gmt_policy.yaml"
    )


def fake_policies_file():
    return "/home/husein/.config/neo-obs/gmt_policy.yaml"


def test_is_policy_exists(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    assert gmt.is_policy_exists() == True


def fake_safe_load(file):
    return {
        "WJV-1": {
            "id": "9f934425b7f5de611c32d6320be45c59",
            "description": "",
            "scheme": {"DC1": "3"},
        },
        "Dual-DC": {
            "id": "926cbd2972ca1d304831d773bebb362c",
            "description": "",
            "scheme": {"DC2": "2", "DC1": "2"},
        },
    }


def fake_notset():
    return "notset"


def test_get_policies(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    monkeypatch.setattr(yaml, "safe_load", fake_safe_load)
    assert gmt.get_policies() == (
        {
            "WJV-1": {
                "id": "9f934425b7f5de611c32d6320be45c59",
                "description": "",
                "scheme": {"DC1": "3"},
            },
            "Dual-DC": {
                "id": "926cbd2972ca1d304831d773bebb362c",
                "description": "",
                "scheme": {"DC2": "2", "DC1": "2"},
            },
        }
    )

    monkeypatch.setattr(gmt, "policies_file", fake_notset)
    assert gmt.get_policies() == "notset"


def fake_request(bucket_name, auth):
    response = mock.Mock()
    response.headers.get.return_value = "dd7e84cfe467c0fc11b5b075ac9acd73"
    return response


def test_policy_id(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_request)
    assert "dd7e84cfe467c0fc11b5b075ac9acd73" == gmt.policy_id(
        "awesome-bucket", auth.plain_auth()
    )


def test_policy_description(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_request)
    assert (
        gmt.policy_description(gmt.policy_id("awesome-bucket", auth.plain_auth()))
        == "Replica Data to all nodes within single Datacenter"
    )

    monkeypatch.setattr(gmt, "policies_file", fake_notset)
    monkeypatch.setattr(requests, "get", fake_request)

    assert None == gmt.policy_description(
        gmt.policy_id("awesome-bucket", auth.plain_auth())
    )
