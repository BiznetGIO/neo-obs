from obs.libs.s3 import requestors
from obs.libs.s3 import get


class TestS3Get:
    def test_doget(self):
        get_params = {
            "object": {"list_objects": {"parameters": {"Bucket": "satu-1828"}}}
        }
        getting_data = get.do_get(json_data=get_params)
        assert getting_data["status_code"] == 400
