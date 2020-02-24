import os
import boto3
import xmltodict

from obs.libs import bucket
from obs.libs import gmt
from obs.libs import auth
from obs.libs import utils
from requests_aws4auth import AWS4Auth
from obs.api.app.helpers.rest import response
from werkzeug.utils import secure_filename
from flask import request, send_file
from flask_restful import Resource, reqparse


def get_resources(access_key, secret_key):
    endpoint = auth.get_endpoint()
    sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = sess.resource("s3", endpoint_url=endpoint)
    return s3_resource


def get_plain_auth(access_key, secret_key):
    auth = AWS4Auth(access_key, secret_key, "eu-west-1", "s3")
    return auth


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
                objects = []
                if buckets["CommonPrefixes"]:
                    for prefix in buckets["CommonPrefixes"]:
                        objects.append({"directory": f"{prefix['Prefix']}"})

                if buckets["Contents"]:
                    for content in buckets["Contents"]:
                        content[
                            "LastModified"
                        ] = f'{content["LastModified"]:%Y-%m-%d %H:%M:%S}'
                        objects.append(content)
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
        except Exception as exc:
            return response(500, str(exc))


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
        except Exception as exc:
            return response(500, str(exc))

    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("acl", type=str)
        parser.add_argument("policy_id", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        acl = args["acl"] if args["acl"] else "private"
        policy_id = args["policy_id"] if args["policy_id"] else ""

        try:
            responses = bucket.create_bucket(
                auth=get_plain_auth(args["access_key"], secret_key),
                bucket_name=bucket_name,
                acl=acl,
                policy_id=policy_id,
            )
            if responses.text:
                error = xmltodict.parse(responses.text)
                return response(400, error["Error"]["Message"])
            return response(201)
        except Exception as exc:
            return response(500, str(exc))

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.remove_bucket(
                get_resources(args["access_key"], secret_key), bucket_name
            )
            return response(204)
        except Exception as exc:
            return response(500, str(exc))


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
        except Exception as exc:
            return response(500, str(exc))

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.remove_object(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
            )
            return response(204)
        except Exception as exc:
            return response(500, str(exc))


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
            return response(204)
        except Exception as exc:
            return response(500, str(exc))


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
            return response(204)
        except Exception as exc:
            return response(500, str(exc))


class download_object(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("object_name", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.download_object(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["object_name"],
            )
            file = send_file(f"/app/obs/api/{args['object_name']}", as_attachment=True)
            return file
        except Exception as exc:
            return response(500, str(exc))


class upload_object(Resource):
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
        file.save(filename)

        object_name = args["object_name"] if args["object_name"] else filename

        try:
            bucket.upload_object(
                resource=get_resources(args["access_key"], secret_key),
                bucket_name=bucket_name,
                local_path=filename,
                object_name=object_name,
            )
            os.remove(filename)

            if args["acl"]:
                bucket.set_acl(
                    resource=get_resources(args["access_key"], secret_key),
                    bucket_name=bucket_name,
                    object_name=object_name,
                    acl_type="object",
                    acl=args["acl"],
                )
            return response(201)
        except Exception as exc:
            return response(500, str(exc))


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
        except Exception as exc:
            return response(500, str(exc))


class acl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("bucket_name", type=str, required=True)
        parser.add_argument("object_name", type=str)
        parser.add_argument("acl", type=str)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        acl_type = "object" if args["object_name"] else "bucket"
        acl = args["acl"] if args["acl"] else "private"

        try:
            bucket.set_acl(
                resource=get_resources(args["access_key"], secret_key),
                bucket_name=args["bucket_name"],
                object_name=args["object_name"],
                acl_type=acl_type,
                acl=acl,
            )
            return response(204)
        except Exception as exc:
            return response(500, str(exc))


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
        except Exception as exc:
            return response(500, str(exc))


class mkdir(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("secret_key", type=str, required=True)
        parser.add_argument("directory", type=str, required=True)
        args = parser.parse_args()
        secret_key = args["secret_key"].replace(" ", "+")

        try:
            bucket.mkdir(
                get_resources(args["access_key"], secret_key),
                bucket_name,
                args["directory"],
            )
            return response(201)
        except Exception as exc:
            return response(500, str(exc))


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
        except Exception as exc:
            return response(500, str(exc))
