import pytest
import mock
import uuid
from obs.libs import gmt
from obs.libs import bucket


@pytest.fixture
def resource(self):
    pass


class Testbucket:
    def fake_resource(self):
        resource = mock.Mock()
        resource.buckets.all.return_value = ["bucket-one", "satu-b21f6bb7-39d5"]
        resource.Bucket.return_value.objects.filter.return_value = [
            "bucket-one",
            "obj.png",
        ]
        return resource

    def test_buckets(self):
        assert bucket.buckets(self.fake_resource()) == [
            "bucket-one",
            "satu-b21f6bb7-39d5",
        ]

    def test_random(self, monkeypatch):
        monkeypatch.setattr(uuid, "uuid4", lambda: "71e43e94-c10d")
        assert bucket.gen_random_name("awesome") == f"awesome-71e43e94-c10d"

    def test_get(self):
        assert bucket.get_objects(self.fake_resource(), "satu-b21f6bb7-39d5") == [
            "bucket-one",
            "obj.png",
        ]

    def fake_objects(self, resource, bucket_name):
        obj1 = mock.Mock()
        obj1.key = "ddg.png"
        obj1.size = 234

        obj2 = mock.Mock()
        obj2.key = "obj.txt"
        obj2.size = 793

        return [obj1, obj2]

    def test_exists(self, monkeypatch):
        monkeypatch.setattr(bucket, "get_objects", self.fake_objects)
        assert bucket.is_exists(resource, "satu", "ddg.png") == True

        assert bucket.is_exists(resource, "satu", "ang.png") == False

    def test_bucket_usage(self, monkeypatch):
        monkeypatch.setattr(bucket, "get_objects", self.fake_objects)
        assert bucket.bucket_usage(resource, "bucket-name") == (1027, 2)

    def fake_bucket(self, resource):
        buckets = []
        for count in range(3):
            bucket = mock.Mock()
            bucket.name = f"bucket{count}"
            buckets.append(bucket)
        return buckets

    def fake_usage(self, resource, name):
        bucket = mock.Mock()
        # number 3 is used to add bucket number with 3
        # number 273 is used to multiply bucket size with 273
        bucket.objects = int(name[-1]) + 3
        bucket.size = bucket.objects * 273
        return bucket.size, bucket.objects

    def test_disk_usage(self, monkeypatch):
        monkeypatch.setattr(bucket, "buckets", self.fake_bucket)
        monkeypatch.setattr(bucket, "bucket_usage", self.fake_usage)
        assert bucket.disk_usage("boom") == [
            ["bucket0", (819, 3)],
            ["bucket1", (1092, 4)],
            ["bucket2", (1365, 5)],
        ]

    def fake_cors(self):
        fake = mock.Mock()
        fake.Cors.return_value.cors_rules = "1jfe"
        return fake

    def test_cors(self):
        assert bucket.get_cors(self.fake_cors()) == "1jfe"

        assert bucket.get_cors("try") == None

    def fake_policy(self):
        fake = mock.Mock()
        fake.Policy.return_value.policy = "newsk"
        return fake

    def test_policy(self):
        assert bucket.get_policy(self.fake_policy()) == "newsk"

        assert bucket.get_policy("try") == None

    def fake_location(self):
        locations = mock.Mock()
        locations.get_bucket_location.return_value = {"LocationConstraint": "Jakarta"}
        return locations

    def test_location(self):
        assert bucket.get_location(self.fake_location(), "bucket-name") == "Jakarta"

    def fake_expire(self):
        fake = mock.Mock()
        fake.get_bucket_lifecycle.return_value = "Expire"
        return fake

    def test_expiration(self):
        assert bucket.get_expiration(self.fake_expire(), "bucket-name") == "Expire"

        assert bucket.get_expiration("try", "bucket-name") == None

    def fake_grant_name(self, types):
        grant = {
            "Grantee": {
                "Type": types,
                "URI": "home/grant/uri/red-deer",
                "DisplayName": "black-deer",
            },
            "Permission": "FULL CONTROL",
        }
        return grant

    def test_grant_name(self):
        assert bucket.get_grant_name(self.fake_grant_name("Group")) == "red-deer"

        assert (
            bucket.get_grant_name(self.fake_grant_name("CanonicalUser")) == "black-deer"
        )

    def fake_grants(self):
        obj = mock.Mock()
        obj.Acl.return_value.grants = [
            self.fake_grant_name("Group"),
            self.fake_grant_name("CanonicalUser"),
        ]
        return obj

    def test_grant(self):
        assert bucket.get_grants(self.fake_grants()) == [
            ["red-deer", "FULL CONTROL"],
            ["black-deer", "FULL CONTROL"],
        ]

    def test_gmt_policy(self, monkeypatch):
        monkeypatch.setattr(gmt, "policy_id", lambda name, auth: None)
        monkeypatch.setattr(
            gmt, "policy_description", lambda id: "Replica Data to all nodes"
        )
        assert (
            bucket.bucket_gmt_policy("bucket-name", "auth")
            == "Replica Data to all nodes"
        )

    def fake_client(self):
        client = mock.Mock()
        client.Bucket.return_value.meta.client = None
        return client

    def test_bucket_info(self, monkeypatch):
        monkeypatch.setattr(
            bucket, "bucket_gmt_policy", lambda name, auth: "Replica Data to all nodes"
        )
        monkeypatch.setattr(bucket, "get_grants", lambda bucket: "123")
        monkeypatch.setattr(bucket, "get_cors", lambda bucket: "None")
        monkeypatch.setattr(bucket, "get_policy", lambda bucket: "None")
        monkeypatch.setattr(bucket, "get_expiration", lambda client, bucket: "None")
        monkeypatch.setattr(bucket, "get_location", lambda client, bucket: "Jakarta")

        assert bucket.bucket_info(self.fake_client(), "bucket-name", "auth") == {
            "ACL": "123",
            "CORS": "None",
            "Policy": "None",
            "Expiration": "None",
            "Location": "Jakarta",
            "GmtPolicy": "Replica Data to all nodes",
        }

    def fake_object_resource(self):
        obj = mock.Mock()
        obj.Object.return_value.storage_class = "Group"
        obj.Object.return_value.content_type = "image/png"
        obj.Object.return_value.content_length = 1280213123
        obj.Object.return_value.last_modified = "2019-09-24 01:01:00"
        obj.Object.return_value.e_tag = "967bd45c88a91f829755742752fe9932"
        return obj

    def test_object_info(self, monkeypatch):
        monkeypatch.setattr(
            bucket, "get_grants", lambda obj: ["red-deer", "FULL CONTROL"]
        )
        assert bucket.object_info(
            self.fake_object_resource(), "bucket-name", "obj-name"
        ) == {
            "ACL": ["red-deer", "FULL CONTROL"],
            "Size": 1280213123,
            "LastModified": "2019-09-24 01:01:00",
            "MD5": "967bd45c88a91f829755742752fe9932",
            "MimeType": "image/png",
            "StorageClass": "Group",
        }

    def fake_url(self):
        client = mock.Mock()
        client.meta.client.generate_presigned_url.return_value = "https://bucket.net"
        return client

    def test_generate_url(self, monkeypatch):
        assert (
            bucket.generate_url(self.fake_url(), "bucket-name", "ddg.png")
            == "https://bucket.net"
        )
