import pytest
from obs.libs import CloudianClient


class TestUser:
    def make_client(self):
        client = CloudianClient(
            url="http://103.77.104.76",
            user="sysadmin",
            password="public",
            port=19443
        )
        return client

    def test_list(self):
        list_params = {
            "groupId": "testing",
            "userType": "all",
            "userStatus": "active"
        }
        list_user = self.make_client().user.list(data=list_params)
        assert list_user['status_code'] == 200

    def test_get(self):
        list_params = {
            "groupId": "testing",
            "userId": "user_264_18957_stage_t2m1",
        }
        get_user = self.make_client().user.get(data=list_params)
        assert get_user['status_code'] == 200

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass
