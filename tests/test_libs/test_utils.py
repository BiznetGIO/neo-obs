import mock
import pytest
import tzlocal
import mock
import xmltodict
from obs.libs import utils


def test_size():
    # 100*13 is used to get size with unit YiB
    assert utils.sizeof_fmt(100 ** 13) == "82.7 YiB"


def test_date(monkeypatch):
    monkeypatch.setattr(tzlocal, "get_localzone", lambda: None)
    assert utils.human_date(0) == f"1970-01-01 00:00:00 ()"


def test_check():
    response = {"reason": "nonsense", "status_code": "valid", "url": ".net"}
    with pytest.raises(ValueError, match=(f"nonsense")):
        utils.check(response)


def fake_response():
    response = mock.Mock()
    response.text = "valid"
    return response


def fake_parse(text):
    response = {"Error": {"Code": "foo", "Message": "False"}}
    return response


def test_check_plain(monkeypatch):
    monkeypatch.setattr(xmltodict, "parse", fake_parse)
    with pytest.raises(ValueError, match=(f"foo: False")):
        utils.check_plain(fake_response())
