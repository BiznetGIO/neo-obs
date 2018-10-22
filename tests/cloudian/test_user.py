import pytest
from obs.libs.cloudian import requestors
from obs.libs.cloudian import user


class TestUser:
    def test_list(self):
        list_params = {
            "groupId": "testing",
            "userType": "all",
            "userStatus": "active"
        }
        list_user = user.list(data=list_params)
        assert list_user['status_code'] == 200

    def test_get(self):
        list_params = {
            "groupId": "testing",
            "userId": "user_264_18957_stage_t2m1",
        }
        get_user = user.get(data=list_params)
        assert get_user['status_code'] == 200

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass
