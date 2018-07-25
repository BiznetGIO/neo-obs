import pytest

from obs.client import CloudianClient


class TestQos:
    def test_get(self):
        client = CloudianClient(
            url="http://103.77.104.76",
            user="sysadmin",
            password="public",
            port=19443
        )
        list_params = {
            "groupId": "testing",
            "userId": "user_264_18957_stage_t2m1",
        }
        list_qos = client.qos.get(data=list_params)
        assert list_qos
