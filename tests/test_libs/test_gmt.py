import os
import mock
import requests
import yaml
import builtins
import pytest
import obs.libs.gmt as gmt
import obs.libs.auth as auth
from obs.libs import config


def fake_policies_file():
    return "gmt_policy.yaml"


def fake_config():
    pass


def test_policies_file(monkeypatch):
    monkeypatch.setattr(config, "load_config_file", fake_config)
    monkeypatch.setattr(os.environ, "get", lambda name: fake_policies_file())
    assert gmt.policies_file() == "gmt_policy.yaml"


def test_exists(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    monkeypatch.setattr(os.path, "isfile", lambda file: True)
    assert gmt.is_policy_exists() == True


def fake_get_policies():
    return {
        "WJV-1": {"id": "1c32d6320", "description": "", "scheme": {"DC1": "3"}},
        "Dual-DC": {
            "id": "d3031d77b",
            "description": "2 Replication in Midplaza, 1 in Technovillage",
            "scheme": {"DC2": "2", "DC1": "2"},
        },
    }


def fake_notset():
    return "notset"


def fake_open(file):
    pass


def test_policies(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    monkeypatch.setattr(gmt, "is_policy_exists", lambda: True)
    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setattr(yaml, "safe_load", lambda file: fake_get_policies())

    assert gmt.get_policies() == (
        {
            "WJV-1": {"id": "1c32d6320", "description": "", "scheme": {"DC1": "3"}},
            "Dual-DC": {
                "id": "d3031d77b",
                "description": "2 Replication in Midplaza, 1 in Technovillage",
                "scheme": {"DC2": "2", "DC1": "2"},
            },
        }
    )


def test_notset(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_notset)
    assert gmt.get_policies() == "notset"


def fake_request(bucket_name, auth):
    response = mock.Mock()
    response.headers.get.return_value = "dd7e84cfe467c0fc11b5b075ac9acd73"
    return response


def fake_auth():
    return ("<requests_aws4auth>", "new.net")


def test_policy_id(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_request)
    assert "dd7e84cfe467c0fc11b5b075ac9acd73" == gmt.policy_id(
        "awesome-bucket", fake_auth()
    )


def test_policy_description(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_get_policies)
    assert (
        gmt.policy_description("d3031d77b")
        == f"2 Replication in Midplaza, 1 in Technovillage"
    )


def test_description_notset(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_notset)
    assert None == gmt.policy_description("d3031d77b")


def test_no_description(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_get_policies)
    assert "No description" == gmt.policy_description("1c32d6320")
