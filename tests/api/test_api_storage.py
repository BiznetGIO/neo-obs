import pytest
import mock

from datetime import datetime
from obs.libs import bucket


def fake_buckets(resource):
    bucket1 = mock.Mock()
    bucket1.name = "bucket-one"
    dt1 = datetime(2019, 9, 24, 1, 1, 0, 0)
    bucket1.creation_date = dt1

    bucket2 = mock.Mock()
    bucket2.name = "bucket-two"
    bucket2.creation_date = dt1

    return [bucket1, bucket2]


def test_list(client, monkeypatch):
    monkeypatch.setattr(bucket, "buckets", fake_buckets)

    result = client.get(
        "/api/storage/list", data={"access_key": "123", "secret_key": "123"}
    )
    assert result.get_json()["data"] == [
        {"name": "bucket-one", "creation_date": "2019-09-24 01:01:00"},
        {"name": "bucket-two", "creation_date": "2019-09-24 01:01:00"},
    ]


def fake_list_objects(resource, bucket_name, prefix=None):
    return {
        "Contents": [
            {
                "Key": "foo.txt",
                "LastModified": datetime(2019, 9, 24, 1, 1, 0, 0),
                "ETag": '"d41d8cd98f00b204e9800998ecffake"',
                "Size": 36,
                "StorageClass": "STANDARD",
                "Owner": {
                    "DisplayName": "john doe",
                    "ID": "5ac765187f93d3f1cef810afakefake",
                },
            }
        ],
        "CommonPrefixes": [{"Prefix": "a/b/"}],
    }


def test_list_object(client, monkeypatch):
    monkeypatch.setattr(bucket, "get_objects", fake_list_objects)

    result = client.get(
        "api/storage/list",
        data={"bucket_name": "test", "access_key": "123", "secret_key": "123"},
    )
    assert {"directory": "a/b/"} in result.get_json()["data"]
