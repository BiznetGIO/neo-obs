import requests
import pytest
import mock
import os

from datetime import datetime
from obs.libs import bucket
from werkzeug.datastructures import FileStorage
from obs.api.app.controllers.api import storage


def fake_resource(access_key, secret_key):
    resouce = mock.Mock()
    resouce.Bucket.return_value.delete.side_effect = lambda: {
        "ResponseMetaData": {"RequestId": "e12"}
    }
    resouce.Object.return_value.delete.side_effect = lambda: {
        "ResponseMetaData": {"RequestId": "e12"}
    }
    resouce.Object.return_value.download_file.side_effect = lambda: ""
    resouce.Object.return_value.upload_file.side_effect = lambda Filename: ""
    resouce.Object.return_value.copy.side_effect = lambda source: ""
    return resouce


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


def fake_list_objects(resource, bucket_name, prefix=""):
    content = {
        "Contents": [
            {
                "Key": "foo.txt",
                "LastModified": datetime(2019, 9, 24, 1, 1, 0, 0),
                "ETag": '"d41d8cd98f00b204e9800998ecffake"',
                "Size": 36,
                "StorageClass": "STANDARD",
            }
        ],
        "CommonPrefixes": [{"Prefix": "a/b/"}],
    }
    return content


def test_list_object(client, monkeypatch):
    monkeypatch.setattr(bucket, "get_objects", fake_list_objects)

    result = client.get(
        "api/storage/list",
        data={"bucket_name": "test", "access_key": "123", "secret_key": "123"},
    )
    assert {"directory": "a/b/"} in result.get_json()["data"]


def test_remove_bucket(client, monkeypatch):
    monkeypatch.setattr(storage, "get_resources", fake_resource)

    result = client.delete(
        "/api/storage/bucket/name", data={"access_key": "123", "secret_key": "123"}
    )
    assert "RequestId" in result.get_json()["data"]["ResponseMetaData"]
    assert result.get_json()["message"] == f"Bucket name deleted successfully."


def test_remove_object(client, monkeypatch):
    monkeypatch.setattr(storage, "get_resources", fake_resource)
    monkeypatch.setattr(bucket, "is_exists", lambda res, bucket, object: True)

    result = client.delete(
        "/api/storage/object/name",
        data={"access_key": "123", "secret_key": "123", "object_name": "object.png"},
    )
    assert "RequestId" in result.get_json()["data"]["ResponseMetaData"]
    assert result.get_json()["message"] == f"Object object.png deleted successfully."


def fake_object(resource, bucket_name, prefix=""):
    content = {
        "Contents": [
            {
                "Key": "obj1.jpg",
                "LastModified": datetime(2019, 9, 24, 1, 1, 0, 0),
                "ETag": '"d41d8cd98f00b204e9800998ecffake"',
                "Size": 36,
                "StorageClass": "STANDARD",
            }
        ],
        "CommonPrefixes": None,
    }
    return content


def test_download(client, monkeypatch, fs):
    def download(access_key, secret_key):
        fs.create_file("/app/obs/api/Downloads/obj1.jpg")
        resource = mock.Mock()
        resource.Object.return_value.download_file.side_effect = lambda name: None
        return resource

    monkeypatch.setattr(bucket, "get_objects", fake_object)
    monkeypatch.setattr(storage, "get_resources", download)
    monkeypatch.setattr(bucket, "is_exists", lambda resource, bucket, object: True)

    result = client.get(
        "/api/storage/object/download/tes_bucket",
        data={"access_key": "123", "secret_key": "123", "object_name": "obj1.jpg"},
    )
    assert "obj1.jpg" in result.headers["Content-Disposition"]
    assert result.status_code == 200


def test_upload(client, monkeypatch, fs):
    fs.create_file("upload/obj1.png")
    file = FileStorage(
        filename="obj1.png",
        content_type="image/png",
        stream=open("upload/obj1.png", "rb"),
    )

    monkeypatch.setattr(storage, "get_resources", fake_resource)

    result = client.post(
        "/api/storage/object/upload/name",
        data={
            "access_key": "123",
            "secret_key": "123",
            "object_name": "/folder/obj1.jpg",
            "acl": "public",
            "files": file,
        },
        content_type="multipart/form-data",
    )
    assert "obj1.png" in os.listdir("/upload")
    assert (
        result.get_json()["message"]
        == f"Object /folder/obj1.jpg uploaded successfully."
    )


def fake_acl(access_key, secret_key):
    acl = mock.Mock()
    acl.info = [[["Test user"], ["FULL_CONTROL"]]]
    acl.Bucket.return_value.Acl.return_value.put.return_value = {
        "ResponseMetaData": {"RequestId": "e12"}
    }
    return acl


def test_acl(client, monkeypatch):
    monkeypatch.setattr(storage, "get_resources", fake_acl)

    result = client.post(
        "/api/storage/acl",
        data={"access_key": "123", "secret_key": "123", "bucket_name": "foo"},
    )
    assert "RequestId" in result.get_json()["data"]["ResponseMetaData"]


def test_mkdir(client, monkeypatch, fs):
    def mkdir(client, monkeypatch):
        fs.create_dir("new")
        resource = mock.Mock()
        resource.meta.client.put_object.return_value = {
            "ResponseMetaData": {"RequestId": "e12"}
        }
        return resource

    monkeypatch.setattr(storage, "get_resources", mkdir)

    result = client.post(
        "/api/storage/mkdir/bucket_name",
        data={"access_key": "123", "secret_key": "123", "directory": "foo"},
    )
    assert "new" in os.listdir("/")
    assert "RequestId" in result.get_json()["data"]["ResponseMetaData"]
    assert result.get_json()["message"] == f"Directory foo added successfully."


def fake_create_bucket(*args, **kwargs):
    request = mock.Mock()
    request.text = None
    return request


def test_create_bucket(client, monkeypatch):
    monkeypatch.setattr(requests, "put", fake_create_bucket)

    result = client.post(
        "/api/storage/bucket/bucket-name",
        data={"access_key": "123", "secret_key": "123"},
    )
    assert result.get_json()["message"] == f"Bucket bucket-name created successfully."


def test_copy(client, monkeypatch):
    monkeypatch.setattr(storage, "get_resources", fake_resource)

    result = client.post(
        "/api/storage/object/copy/bucket_name",
        data={
            "access_key": "123",
            "secret_key": "123",
            "object_name": "obj.png",
            "copy_to": "bucket2",
        },
    )
    assert result.get_json()["message"] == f"Object obj.png copied successfully."
