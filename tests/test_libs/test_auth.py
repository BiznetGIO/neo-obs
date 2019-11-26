import mock
import boto3
from obs.libs import auth
from obs.libs import config


def fake_config():
    pass


def fake_session(**kwargs):
    session = mock.Mock()
    session.resource.return_value = "s3_resource"
    return session


def test_resource(monkeypatch):
    monkeypatch.setattr(config, "load_config_file", fake_config)
    monkeypatch.setattr(boto3, "Session", fake_session)
    assert auth.resource() == "s3_resource"
