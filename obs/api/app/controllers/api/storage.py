import os
import re
import boto3
import zipfile
import tempfile
import xmltodict

from obs.libs import bucket
from obs.libs import gmt
from obs.libs import auth
from obs.libs import utils
from requests_aws4auth import AWS4Auth
from obs.api.app.helpers.rest import response
from werkzeug.utils import secure_filename
from flask import request, current_app, send_from_directory
from flask_restful import Resource, reqparse


def get_resources(access_key, secret_key):
    endpoint = auth.get_endpoint("storage")
    sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = sess.resource("s3", endpoint_url=endpoint)
    return s3_resource


def get_plain_auth(access_key, secret_key):
    auth = AWS4Auth(access_key, secret_key, "eu-west-1", "s3")
    return auth


def list_objects(buckets, contents="Contents", date="LastModified"):
    objects = []
    if buckets["CommonPrefixes"]:
        for prefix in buckets["CommonPrefixes"]:
            objects.append({"directory": f"{prefix['Prefix']}"})

    if buckets[contents]:
        for content in buckets[contents]:
            content[date] = f"{content[date]:%Y-%m-%d %H:%M:%S}"
            objects.append(content)
    return objects


class list(Resource):
    def get(self, prefix=""):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("bucket_name", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        bucket_name = args["bucket_name"]
        if args["bucket_name"]:
            bucket_name, prefix = utils.get_bucket_key(args["bucket_name"])

        try:
            if args["bucket_name"]:
                buckets = bucket.get_objects(
                    get_resources(args["access_key"], secret_key), bucket_name, prefix
                )
                objects = list_objects(buckets)
                if not objects:
                    return response(200, f"Bucket is Empty.")
                return response(200, data=objects)

            buckets = bucket.buckets(get_resources(args["access_key"], secret_key))
            all_bucket = []
            for index, buck in enumerate(buckets):
                all_bucket.append(
                    {
                        "name": buck.name,
                        "creation_date": f"{buck.creation_date:%Y-%m-%d %H:%M:%S}",
                    }
                )
            if not all_bucket:
                return response(200, f"Storage is Empty.")
            return response(200, data=all_bucket)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class bucket_api(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket_info = bucket.bucket_info(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                get_plain_auth(args["access_key"], secret_key),
            )
            return response(200, data=bucket_info)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("acl", type=str, default="private")
        parser.add_argument("policy_id", type=str, default="")
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            regex = r"[^a-z0-9.-]"
            bucket_name = re.sub(regex, "", bucket_name)
            current_app.logger.error(len(bucket_name))
            if not 2 < len(bucket_name) < 64:
                return response(
                    400, f"'{bucket_name}' too short or too long for bucket name"
                )

            current_app.logger.error(len(bucket_name))
            responses = bucket.create_bucket(
                auth=get_plain_auth(args["access_key"], secret_key),
                bucket_name=bucket_name,
                acl=args["acl"],
                policy_id=args["policy_id"],
            )
            if responses.text:
                error = xmltodict.parse(responses.text)
                return response(400, error["Error"]["Message"])
            return response(201, f"Bucket {bucket_name} created successfully.")
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            result = bucket.remove_bucket(
                get_resources(args["access_key"], secret_key), bucket_name
            )
            return response(200, f"Bucket {bucket_name} deleted successfully.", result)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class object_api(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            object_info = bucket.object_info(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
            )
            for key, value in object_info.items():
                object_info[key] = f"{value}"
            return response(200, data=object_info)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            result = bucket.remove_object(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
            )
            return response(
                200, f"Object {args['object_name']} deleted successfully.", result
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class move_object(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        parser.add_argument("move_to", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.move_object(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
                args["move_to"],
                None,
            )
            return response(201, f"Object {args['object_name']} moved successfully.")
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class copy_object(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        parser.add_argument("copy_to", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.copy_object(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
                args["copy_to"],
                None,
            )
            return response(201, f"Object {args['object_name']} copied successfully.")
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


def file_download(resources, bucket_name, prefix):
    status = bucket.get_objects(resources, bucket_name, prefix)
    status = list_objects(status)
    for obj in status:
        if "Key" in obj and obj["Key"][-1] != "/":
            bucket.download_object(resources, bucket_name, obj["Key"])
        if "directory" in obj:
            file_download(resources, bucket_name, obj["directory"])


def archive(dir_name):
    with zipfile.ZipFile(f"{dir_name[:-1]}.zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk("."):
            for file in files:
                file_path = os.path.join(root, file)
                if "zip" not in file:
                    zip_file.write(file_path, file_path.replace(dir_name, ""))
    return f"{dir_name[:-1]}.zip"


class download_object(Resource):
    def get(self, bucket_name, name=""):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, default="")
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        with tempfile.TemporaryDirectory() as tempdir:
            try:
                os.chdir(tempdir)

                resources = get_resources(args["access_key"], secret_key)
                file_download(resources, bucket_name, args["object_name"])

                if args["object_name"] == "":
                    name = archive(bucket_name + "/")
                elif args["object_name"][-1] == "/":
                    name = archive(args["object_name"])
                else:
                    name = args["object_name"]
                file = send_from_directory(tempdir, name, as_attachment=True)
                return file
            except Exception as e:
                current_app.logger.error(f"{e}")
                return response(500, f"{e}")


class upload_object(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, default="")
        parser.add_argument("upload_id", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            if args["upload_id"]:
                parts = bucket.list_part(
                    get_resources(args["access_key"], secret_key),
                    bucket_name,
                    args["object_name"],
                    args["upload_id"],
                )
                if parts is None:
                    return response(404, f"Part not found, please abort this object.")
                for part in parts:
                    part["LastModified"] = f'{part["LastModified"]:%Y-%m-%d %H:%M:%S}'
                return response(201, data=parts)

            mpu = bucket.list_multipart_upload(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
            )
            lmpu = list_objects(mpu, "Uploads", "Initiated")
            return response(201, data=mpu)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        parser.add_argument("upload_id", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            mpu = bucket.abort_multipart_upload(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
                args["upload_id"],
            )
            return response(
                201,
                f"Multipart upload for {args['object_name']} has been aborted.",
                mpu,
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def put(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        parser.add_argument("upload_id", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            mpu = bucket.complete_multipart_upload(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
                args["upload_id"],
            )
            return response(
                201, f"Multipart upload for {args['object_name']} has been completed."
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")

    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str)
        parser.add_argument("acl", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        file = request.files["files"]
        filename = secure_filename(file.filename)
        object_name = args["object_name"] if args["object_name"] else filename

        try:
            regex = r"[\"\{}^%`\]\[~<>|#]|[^\x00-\x7F]"
            object_name = re.sub(regex, "", object_name)

            result = bucket.upload_bin_object(
                resource=get_resources(args["access_key"], secret_key),
                bucket_name=bucket_name,
                fileobj=file,
                object_name=object_name,
                content_type=file.content_type,
            )
            if args["acl"]:
                bucket.set_acl(
                    resource=get_resources(args["access_key"], secret_key),
                    bucket_name=bucket_name,
                    object_name=object_name,
                    acl_type="object",
                    acl=args["acl"],
                )
            return response(201, f"Object {object_name} uploaded successfully.", result)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class usage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("bucket_name", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            if args["bucket_name"]:
                total_size, total_objects = bucket.bucket_usage(
                    get_resources(args["access_key"], secret_key), args["bucket_name"]
                )
                bucket_usage = {
                    "name": args["bucket_name"],
                    "size": total_size,
                    "objects": total_objects,
                }
                return response(200, data=bucket_usage)

            disk_usage = {"bucket": [], "total_usage": 0}
            disk_usages = bucket.disk_usage(
                get_resources(args["access_key"], secret_key)
            )
            for usage in disk_usages:
                bucket_name = usage[0]
                total_size, total_objects = usage[1]
                disk_usage["total_usage"] += total_size
                disk_usage["bucket"].append(
                    {"name": bucket_name, "size": total_size, "objects": total_objects}
                )
            disk_usage["total_usage"] = f"{disk_usage['total_usage']}"
            return response(200, data=disk_usage)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class acl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("bucket_name", type=str, required=True)
        parser.add_argument("object_name", type=str)
        parser.add_argument("acl", type=str, default="private")
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        acl_type = "object" if args["object_name"] else "bucket"
        name = args["object_name"] if args["object_name"] else args["bucket_name"]

        try:
            result = bucket.set_acl(
                resource=get_resources(args["access_key"], secret_key),
                bucket_name=args["bucket_name"],
                object_name=args["object_name"],
                acl_type=acl_type,
                acl=args["acl"],
            )
            return response(
                200, f"Added {args['acl']} access to {acl_type} {name}.", result
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class presign(Resource):
    def get(self, bucket_name, object_name):
        parser = reqparse.RequestParser()
        parser.add_argument("expire", type=int)
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            url = bucket.generate_url(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                object_name,
                args["expire"],
            )
            return response(200, data=url)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class mkdir(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("directory", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            result = bucket.mkdir(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["directory"],
            )
            return response(
                201, f"Directory {args['directory']} added successfully.", result
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")


class gmt_policy(Resource):
    def get(self):
        try:
            msg = []
            policies = gmt.get_policies()

            for zone in policies:
                policy_id, description, _ = policies[zone].values()
                if not description:
                    description = "No description"
                msg.append({"Name": zone, "Id": policy_id, "Description": description})
            return response(200, data=msg)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500, f"{e}")
