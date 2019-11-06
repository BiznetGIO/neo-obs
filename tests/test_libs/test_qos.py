import mock
import pytest
from obs.libs import qos
from obs.libs import auth


@pytest.fixture
def limit():
    return {
        "groupId": "testing",
        "userId": "StageTest",
        "labelId": "qos.userQosOverrides.title",
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
    }


def fake_client():
    client = mock.Mock()
    client.qos.limits.return_value = limit()
    return client


def test_info():
    assert qos.info(fake_client(), "StageTest", "testing") == limit()


def test_set():
    assert qos.set(fake_client(), "user", "group", "limit") == limit()


def test_rm():
    assert qos.rm(fake_client(), "user", "group") == limit()
