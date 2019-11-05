import os
from obs.libs import config


def test_config_file(monkeypatch):
    monkeypatch.setattr(os.path, "expanduser", lambda comment: "home/hors")
    assert config.config_file() == "home/hors/.config/neo-obs/obs.env"


def test_exists(monkeypatch):
    monkeypatch.setattr(config, "config_file", lambda: None)
    monkeypatch.setattr(os.path, "isfile", lambda file: True)
    assert config.is_config_exists() == True
