import pytest
import mock
import os
import requests
import xmltodict
from datetime import datetime

import obs.libs.bucket
import obs.libs.auth
import obs.libs.gmt
import obs.libs.utils
import obs.libs.config
from obs.cli.main import cli
from click.testing import CliRunner


def fake_resource():
    pass


def fake_plain_auth():
    pass


def load_config_file():
    pass


@pytest.fixture
def resource(monkeypatch):
    monkeypatch.setattr(obs.libs.config, "load_config_file", load_config_file)
    monkeypatch.setattr(obs.libs.auth, "resource", fake_resource)


@pytest.fixture
def plain_auth(monkeypatch):
    monkeypatch.setattr(obs.libs.config, "load_config_file", load_config_file)
    monkeypatch.setattr(obs.libs.auth, "plain_auth", fake_plain_auth)


def fake_buckets(resource):
    bucket1 = mock.Mock()
    bucket1.name = "bucket-one"
    dt1 = datetime(2019, 9, 24, 1, 1, 0, 0)
    bucket1.creation_date = dt1

    bucket2 = mock.Mock()
    bucket2.name = "bucket-two"
    bucket2.creation_date = dt1

    return [bucket1, bucket2]


def fake_session(**kwargs):
    session = mock.Mock()
    session.resource.return_value = "s3_resource"
    return session


def test_resources(monkeypatch):
    monkeypatch.setattr(obs.libs.config, "config_file", lambda: "home/user/path")

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "ls"])
    assert result.output == (
        f"[Errno 2] No such file or directory: 'home/user/path'\n"
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one\n"
    )


def test_plain_auth(monkeypatch):
    monkeypatch.setattr(obs.libs.config, "config_file", lambda: "home/user/path")

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "info", "s3://satu/"])
    assert result.output == (
        f"[Errno 2] No such file or directory: 'home/user/path'\n"
        f"Configuration file not available.\n"
        f"Consider running 'obs --configure' to create one\n"
    )


def test_ls(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "buckets", fake_buckets)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "ls"])
    assert result.output == (
        f"2019-09-24 01:01:00 bucket-one\n" f"2019-09-24 01:01:00 bucket-two\n"
    )


def fake_exc_buckets(resource):
    bucket1 = mock.Mock()
    bucket1.name = "bucket-one"
    bucket1.creation_date = "date"

    return [bucket1]


def test_except_ls(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "buckets", fake_exc_buckets)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "ls"])
    assert result.output == (f"Bucket listing failed. \n" f"Invalid format specifier\n")


def fake_get_objects(resource, bucket_name, prefix=None):
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


def test_ls_storage(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "get_objects", fake_get_objects)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "ls", "s3://bucket-two/a/b/"])

    assert "bucket-two/foo.txt" in result.output


def test_empty_storage(monkeypatch, resource):
    monkeypatch.setattr(
        obs.libs.bucket, "get_objects", lambda resource, bucket_name, prefix: ""
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "ls", "bucket-one"])

    assert result.output == (
        f'Bucket "bucket-one" is empty\n' f"string indices must be integers\n"
    )


def fake_get_files(resource, bucket_name, prefix=""):
    obj1 = mock.Mock()
    obj1.key = "ddg.png"
    obj1.size = 234

    obj2 = mock.Mock()
    obj2.key = "obj.txt"
    obj2.size = 793

    return [obj1, obj2]


def test_bucket_usage(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "get_files", fake_get_files)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "du", "s3://bucket-one/"])

    assert result.output == (f'1.00 KiB, 2 objects in "bucket-one" bucket\n')


def fake_bucket_info(resource, bucket_name, auth):
    acl = [[["Test user"], ["FULL_CONTROL"]], [["Public"], ["FULL_CONTROL"]]]
    info = {
        "ACL": acl,
        "CORS": None,
        "Policy": None,
        "Expiration": None,
        "Location": "US",
        "GmtPolicy": "2 Replication in Midplaza, 1 in Technovillage",
    }

    return info


def test_bucket_info(monkeypatch, resource, plain_auth):
    monkeypatch.setattr(obs.libs.bucket, "bucket_info", fake_bucket_info)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "info", "bucket-one"])
    assert result.output == (
        f"Location: US\n"
        f"Expiration Rule: None\n"
        f"Policy: None\n"
        f"CORS: None\n"
        f"ACL: ['Test user'] : ['FULL_CONTROL']\n"
        f"ACL: ['Public'] : ['FULL_CONTROL']\n"
        f"Gmt Policy: 2 Replication in Midplaza, 1 in Technovillage\n"
    )


def fake_exc_bucket_info(resource, bucket_name, auth):
    acl = [["Test user"], ["FULL_CONTROL"]]
    info = {
        "ACL": acl,
        "CORS": None,
        "Policy": None,
        "Expiration": None,
        "Location": "US",
        "GmtPolicy": "2 Replication in Midplaza, 1 in Technovillage",
    }
    return info


def test_except_bucket_info(resource, plain_auth, monkeypatch):
    monkeypatch.setattr(obs.libs.bucket, "bucket_info", fake_exc_bucket_info)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "info", "bucket-one"])

    assert result.output == (
        f"Location: US\n"
        f"Expiration Rule: None\n"
        f"Policy: None\n"
        f"CORS: None\n"
        f"Info fetching failed. \n"
        f"list index out of range\n"
    )


def fake_object_info(resource, bucket_name, object_name):
    acl = [[["Test user"], ["FULL_CONTROL"]]]
    dt = datetime(2019, 9, 24, 13, 18, 7, 0)
    info = {
        "ACL": acl,
        "Size": 300,
        "LastModified": dt,
        "MD5": "5610180790cf66a71cf5ea9ad0f920f5",
        "MimeType": "binary/octet-stream",
        "StorageClass": None,
    }

    return info


def test_object_info(monkeypatch, resource, plain_auth):
    monkeypatch.setattr(obs.libs.bucket, "object_info", fake_object_info)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "info", "s3://bucket-one/logo.png"])

    assert result.output == (
        f"File Size: 300.0 B\n"
        f"Last Modified: 2019-09-24 13:18:07\n"
        f"Mime Type: binary/octet-stream\n"
        f"Storage: None\n"
        "MD5 Sum: 5610180790cf66a71cf5ea9ad0f920f5\n"
        f"ACL: ['Test user'] : ['FULL_CONTROL']\n"
    )


def fake_exc_object_info(resource, bucket_name, object_name):
    info = {
        "ACL": "foo",
        "Size": 300,
        "LastModified": "foo",
        "MD5": "5610180790cf66a71cf5ea9ad0f920f5",
        "MimeType": "binary/octet-stream",
        "StorageClass": None,
    }

    return info


def test_except_object_info(resource, plain_auth, monkeypatch):
    monkeypatch.setattr(obs.libs.bucket, "object_info", fake_exc_object_info)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "info", "s3://bucket-one/logo.png"])

    assert result.output == (f"Info fetching failed. \n" f"Invalid format specifier\n")


def fake_presign(resource, bucket_name, object_name, expire):
    return "https://myendpotin.net/oneoneone/logo.png?AWSAccessKeyId=62fake123&Signature=rSNa6fake&Expires=15"


def test_presign(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "generate_url", fake_presign)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "presign", "s3://bucket-one/logo.png"])

    assert (
        result.output
        == "https://myendpotin.net/oneoneone/logo.png?AWSAccessKeyId=62fake123&Signature=rSNa6fake&Expires=15\n"
    )


def test_except_presign(monkeypatch, resource):

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "presign", "s3://bucket-one/logo.png"])

    assert result.output == (
        f"URL generation failed. \n" f"'NoneType' object has no attribute 'meta'\n"
    )


def create_fake_buck(objsize):
    buck = mock.Mock()
    buck.total_objects = len(objsize)
    buck.total_size = sum(objsize)
    return buck.total_size, buck.total_objects


def fake_disk_usage(resource):
    bucket_name = ["green", "black"]
    disk_usages = []
    buck = []
    buck.append(create_fake_buck([100, 200]))
    buck.append(create_fake_buck([400, 150, 250]))
    for bckt, obj in zip(bucket_name, buck):
        disk_usages.append([bckt, obj])
    return disk_usages


def test_disk_usage(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "disk_usage", fake_disk_usage)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "du"])

    assert result.output == (
        f'300.00 Byte, 2 objects in "green" bucket\n'
        f'800.00 Byte, 3 objects in "black" bucket\n'
        f"---\n"
        f"1.07 KiB Total\n"
    )


def fake_exc_disk_usage(resource):
    bucket_name = ["green", "black"]
    disk_usages = []
    buck = []
    buck.append(create_fake_buck(12))
    buck.append(create_fake_buck(10))
    for bckt, obj in zip(bucket_name, buck):
        disk_usages.append([bckt, obj])
    return disk_usages


def test_except_disk_usage(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.bucket, "disk_usage", fake_exc_disk_usage)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "du"])

    assert result.output == (
        f"Disk usage fetching failed. \n" f"object of type 'int' has no len()\n"
    )


def fake_gmt():
    policies = {
        "Jakarta": {"id": "123", "desc": "", "_": ""},
        "Sydney": {"id": "143", "desc": "foo", "_": ""},
    }
    return policies


def test_gmt(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.gmt, "get_policies", fake_gmt)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "gmt", "--policy-id"])

    assert result.output == (
        f"Name: Jakarta\n"
        f"Id: 123\n"
        f"Description: No description\n\n"
        f"Name: Sydney\n"
        f"Id: 143\n"
        f"Description: foo\n\n"
    )


def test_notset_gmt(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.gmt, "get_policies", lambda: "notset")

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "gmt", "--policy-id"])

    assert result.output == (
        f"Can't find Policy file\n"
        f"See '#using-cloudian-hyperstore-extension' in our documentation for more information\n"
    )


def test_except_gmt(monkeypatch, resource):
    monkeypatch.setattr(obs.libs.gmt, "get_policies", lambda: {"foo": "bar"})

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "gmt", "--policy-id"])

    assert result.output == (
        f"Show policies failed. \n" f"'str' object has no attribute 'values'\n"
    )


def fake_move():
    bucket = mock.Mock()
    bucket.Object.return_value.copy.side_effect = lambda source: None
    bucket.Object.return_value.delete.side_effect = lambda: None
    return bucket


def test_mv(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_move)
    monkeypatch.setattr(obs.libs.bucket, "is_exists", lambda res, bucket, object: True)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["storage", "mv", "s3://bucket-one/obj1", "s3://bucket-two"]
    )

    assert result.output == f'Object "obj1" moved to "bucket-two" bucket successfully\n'


def test_except_mv(monkeypatch, resource):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_move)
    monkeypatch.setattr(obs.libs.bucket, "is_exists", lambda res, bucket, object: False)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["storage", "mv", "s3://bucket-one/obj1", "s3://bucket-two"]
    )

    assert result.output == (f"Object move failed. \n" f"Object not exists: obj1\n")


def fake_copy():
    bucket = mock.Mock()
    bucket.Object.return_value.copy.side_effect = lambda source: None
    return bucket


def test_cp(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_copy)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["storage", "cp", "s3://bucket-one/obj1", "s3://bucket-two/"]
    )

    assert result.output == f'Object "obj1" copied successfully\n'


def test_except_cp(resource):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["storage", "cp", "s3://bucket-one/obj1", "s3://bucket-two/"]
    )

    assert result.output == (
        f"Object copy failed. \n" f"'NoneType' object has no attribute 'Object'\n"
    )


def fake_remove():
    bucket = mock.Mock()
    bucket.Object.return_value.delete.side_effect = lambda: None
    return bucket


def test_rm_object(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_remove)
    monkeypatch.setattr(obs.libs.bucket, "is_exists", lambda res, bucket, object: True)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "rm", "s3://bucket-one/obj1"])

    assert result.output == f'Object "obj1" removed successfully\n'


def test_except_rm_object(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_remove)
    monkeypatch.setattr(obs.libs.bucket, "is_exists", lambda res, bucket, object: False)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "rm", "s3://bucket-one/obj1"])

    assert result.output == (f"Object removal failed. \n" f"Object not exists: obj1\n")


def fake_mb(*args, **kwargs):
    requests = mock.Mock()
    requests.put.side_effect = lambda: None
    return requests


def test_mb(monkeypatch, plain_auth):
    monkeypatch.setattr(obs.libs.auth, "strtobool", lambda http: True)
    monkeypatch.setattr(requests, "put", fake_mb)
    monkeypatch.setattr(obs.libs.utils, "check_plain", lambda response: None)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "mb", "bucket-one", "--random"])

    assert result.output == f'Bucket "bucket-one" created successfully\n'


def fake_response(**kwargs):
    response = mock.Mock()
    response.text = "Done"
    return response


def test_except_mb(monkeypatch, plain_auth):
    monkeypatch.setattr(obs.libs.bucket, "create_bucket", fake_response)
    monkeypatch.setattr(
        xmltodict,
        "parse",
        lambda response: {"Error": {"Code": "101", "Message": "Error"}},
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "mb", "bucket-one"])

    assert result.output == (f"Bucket creation failed. \n" f"101: Error\n")


def fake_remove_bucket():
    bucket = mock.Mock()
    bucket.Bucket.return_value.delete.side_effect = lambda: None
    return bucket


def test_rm_bucket(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_remove_bucket)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "rm", "s3://bucket-one/"])

    assert result.output == f'Bucket "bucket-one" deleted successfully.\n'


def test_except_rm_bucket(monkeypatch, resource):
    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "rm", "bucket-one"])

    assert result.output == f"'NoneType' object has no attribute 'Bucket'\n"


def fake_acl_object():
    acl = mock.Mock()
    acl.info = []
    acl.Object.return_value.Acl.return_value.put.side_effect = acl.info.append(
        [["Testing"], ["FULL_CONTROL"]]
    )
    return acl


def fake_acl_Bucket():
    acl = mock.Mock()
    acl.info = [[["Test user"], ["FULL_CONTROL"]]]
    acl.Bucket.return_value.Acl.return_value.put.side_effect = acl.info.append(
        [["Testing"], ["FULL_CONTROL"]]
    )
    return acl


def test_acl_bucket(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_acl_Bucket)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "acl", "bucket-one", "private"])

    assert fake_acl_Bucket().info == [
        [["Test user"], ["FULL_CONTROL"]],
        [["Testing"], ["FULL_CONTROL"]],
    ]
    assert result.output == f"ACL changed successfully\n"


def test_acl_object(monkeypatch):
    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", fake_acl_object)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "acl", "s3://bucket-one/obj1", "private"])
    assert fake_acl_object().info == [[["Testing"], ["FULL_CONTROL"]]]

    assert result.output == f"ACL changed successfully\n"


def test_except_acl(resource):
    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "acl", "bucket-one", "private"])

    assert result.output == (
        f"ACL change failed. \n" f"'NoneType' object has no attribute 'Bucket'\n"
    )


def test_get(monkeypatch, fs, resource):
    def donwload():
        fs.create_file("/obj1.jpg")
        resource = mock.Mock()
        resource.Object.return_value.download_file.side_effect = lambda name: None
        return resource

    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", donwload)
    monkeypatch.setattr(
        obs.libs.bucket, "is_exists", lambda resource, bucket, object: True
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "get", "s3://bucket-one/obj1.jpg"])

    assert os.path.exists("/obj1.jpg")
    assert result.output == f'Object "obj1.jpg" downloaded successfully\n'


def test_except_get(monkeypatch, resource):
    monkeypatch.setattr(
        obs.libs.bucket, "is_exists", lambda resource, bucket, object: False
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "get", "s3://bucket-one/obj1.png"])

    assert result.output == (f"Object download failed. \nObject not exists: obj1.png\n")


def test_put(monkeypatch, fs, resource):
    def upload(**kwargs):
        fs.create_file("upload/obj1.png")

    monkeypatch.setattr(obs.libs.bucket, "upload_object", upload)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["storage", "put", "obj1.png", "s3://bucket-one/obj1.png"]
    )

    assert os.path.exists("upload/obj1.png")
    assert result.output == f'Object "obj1.png" uploaded successfully\n'


def fake_dir():
    resource = mock.Mock()
    resource.meta.client.put_object.side_effect = lambda **kwargs: "done"
    return resource


def test_mkdir(monkeypatch, fs):
    def mkdir():
        fs.create_dir("/new/")
        resource = mock.Mock()
        resource.meta.client.put_object.side_effect = lambda **kwargs: None
        return resource

    monkeypatch.setattr(obs.cli.storage.commands, "get_resources", mkdir)

    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "mkdir", "s3://bucket-one/obs"])

    assert os.path.exists("/new/")
    assert result.output == f'Directory "obs" created successfully\n'


def test_except_mkdir(resource):
    runner = CliRunner()
    result = runner.invoke(cli, ["storage", "mkdir", "s3://bucket-one/obs"])
    assert result.output == (
        f"Directory creation failed. \n" f"'NoneType' object has no attribute 'meta'\n"
    )
