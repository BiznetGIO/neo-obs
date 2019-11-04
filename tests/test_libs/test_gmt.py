import os, mock, requests, yaml, builtins, pytest
import obs.libs.gmt as gmt
import obs.libs.auth as auth
from obs.libs import config


def fake_policy_exists():
    return True


def fake_policies_file():
    return "gmt_policy.yaml"


def fake_config():
    pass


def fake_environ(name):
    return fake_policies_file()


def test_policies_file(monkeypatch):
    monkeypatch.setattr(config, "load_config_file", fake_config)
    monkeypatch.setattr(os.environ, "get", fake_environ)
    assert gmt.policies_file() == "gmt_policy.yaml"


def fake_path(file):
    return True


def test_exists(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    monkeypatch.setattr(os.path, "isfile", fake_path)
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


def fake_yaml(file):
    return fake_get_policies()


def fake_notset():
    return "notset"


def fake_open(file):
    pass


def test_policies(monkeypatch):
    monkeypatch.setattr(gmt, "policies_file", fake_policies_file)
    monkeypatch.setattr(gmt, "is_policy_exists", fake_policy_exists)
    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setattr(yaml, "safe_load", fake_yaml)

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
    return ("<requests_aws4auth>", "biznetgio.net")


def test_policy_id(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_request)
    assert "dd7e84cfe467c0fc11b5b075ac9acd73" == gmt.policy_id(
        "awesome-bucket", fake_auth()
    )


def test_policy_description(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_get_policies)
    assert (
        gmt.policy_description("d3031d77b")
        == "2 Replication in Midplaza, 1 in Technovillage"
    )


def test_description_notset(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_notset)
    assert None == gmt.policy_description("d3031d77b")


def test_no_description(monkeypatch):
    monkeypatch.setattr(gmt, "get_policies", fake_get_policies)
    assert "No description" == gmt.policy_description("1c32d6320")
