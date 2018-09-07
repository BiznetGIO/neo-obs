import pytest
from obs.libs.cloudian import qos

class TestQos:
    def test_get(self):
        list_params = {
            "groupId": "testing",
            "userId": "user_264_18957_stage_t2m1",
        }
        list_qos = qos.get(data=list_params)
        print(list_qos)
        assert list_qos
