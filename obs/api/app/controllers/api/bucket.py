import bitmath
import obs.libs.gmt as bucket_gmt
import obs.libs.bucket as bucket
import obs.libs.auth as auth

from obs.libs import utils
from app.helpers.rest import response
from flask import request, jsonify
from flask_restful import Resource, reqparse


def get_resources():
    return auth.resource()


def get_plain_auth():
    return auth.plain_auth()


class list(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bucket_name", type=str)
        args = parser.parse_args()

        try:
            if args["bucket_name"]:
                buckets = bucket.get_objects(get_resources(), args["bucket_name"], "")

                objects = []
                if buckets["CommonPrefixes"]:
                    for prefix in buckets["CommonPrefixes"]:
                        print(prefix)
                        objects.append({"directory": f"{prefix['Prefix']}"})

                if buckets["Contents"]:
                    for content in buckets["Contents"]:
                        last_modified = content["LastModified"]
                        objects.append(
                            {
                                "modified": f"{last_modified:%Y-%m-%d %H:%M:%S}",
                                "size": f"{content['Size']}",
                                "object_name": f"{content['Key']}",
                            }
                        )
                return response(200, data=objects)

            buckets = bucket.buckets(get_resources())
            all_bucket = []
            for index, buck in enumerate(buckets):
                all_bucket.append(
                    {
                        "name": buck.name,
                        "creation_date": f"{buck.creation_date:%Y-%m-%d %H:%M:%S}",
                    }
                )
            return response(200, data=all_bucket)
        except Exception:
            return response(500)


class bucket_api(Resource):
    def get(self, bucket_name):
        try:
            bucket_info = bucket.bucket_info(
                get_resources(), bucket_name, get_plain_auth()
            )
            return response(200, data=bucket_info)
        except Exception:
            return response(500)

    def post(self, bucket_name):
        try:
            bucket.create_bucket(auth=get_plain_auth(), bucket_name=bucket_name)
            return response(201)
        except Exception:
            return response(500)

    def delete(self, bucket_name):
        try:
            bucket.remove_bucket(get_resources(), bucket_name)
            return response(204)
        except Exception:
            return response(500)


class object_api(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        args = parser.parse_args()

        try:
            object_info = bucket.object_info(
                get_resources(), bucket_name, args["object_name"]
            )
            for key, value in object_info.items():
                object_info[key] = f"{value}"
            return response(200, data=object_info)
        except Exception:
            return response(500)

    def delete(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        args = parser.parse_args()

        try:
            bucket.remove_object(get_resources(), bucket_name, args["object_name"])
            return response(204)
        except Exception:
            return response(500)


class move_object(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        parser.add_argument("move_to", type=str)
        args = parser.parse_args()
        try:
            bucket.move_object(
                get_resources(), bucket_name, args["object_name"], args["move_to"], None
            )
            return response(204)
        except Exception:
            return response(500)


class copy_object(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        parser.add_argument("copy_to", type=str)
        args = parser.parse_args()

        try:
            bucket.copy_object(
                get_resources(), bucket_name, args["object_name"], args["copy_to"], None
            )
            return response(204)
        except Exception:
            return Exception


class download_object(Resource):
    def get(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        args = parser.parse_args()

        try:
            bucket.download_object(get_resources(), bucket_name, args["object_name"])
            return response(204)
        except Exception:
            return response(500)


class upload_object(Resource):
    def post(self, bucket_name):
        parser = reqparse.RequestParser()
        parser.add_argument("object_name", type=str)
        parser.add_argument("path", type=str)
        args = parser.parse_args()

        try:
            bucket.upload_object(
                resource=get_resources(),
                bucket_name=bucket_name,
                local_path=args["path"],
                object_name=args["object_name"],
            )

            return response(201)
        except Exception:
            return Exception


class usage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bucket_name", type=str)
        args = parser.parse_args()

        try:
            if args["bucket_name"]:
                total_size, total_objects = bucket.bucket_usage(
                    get_resources(), args["bucket_name"]
                )
                bucket_usage = {
                    "name": args["bucket_name"],
                    "size": total_size,
                    "objects": total_objects,
                }
                return response(200, data=bucket_usage)

            disk_usage = {"bucket": [], "total_usage": 0}
            disk_usages = bucket.disk_usage(get_resources())
            for usage in disk_usages:
                bucket_name = usage[0]
                total_size, total_objects = usage[1]
                disk_usage["total_usage"] += total_size
                disk_usage["bucket"].append(
                    {"name": bucket_name, "size": total_size, "objects": total_objects}
                )
            return response(200, data=disk_usage)
        except Exception:
            return Exception


class acl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bucket_name", type=str, required=True)
        parser.add_argument("object_name", type=str)
        parser.add_argument("acl", type=str)
        args = parser.parse_args()

        acl_type = "object" if args["object_name"] else "bucket"
        acl = args["acl"] if args["acl"] else "private"

        try:
            bucket.set_acl(
                resource=get_resources(),
                bucket_name=args["bucket_name"],
                object_name=args["object_name"],
                acl_type=acl_type,
                acl=acl,
            )
            return response(204)
        except Exception:
            return response(500)


class presign(Resource):
    def get(self, bucket_name, object_name):
        parser = reqparse.RequestParser()
        parser.add_argument("expire", type=int)
        args = parser.parse_args()

        try:
            url = bucket.generate_url(
                get_resources(), bucket_name, object_name, args["expire"]
            )
            return response(200, data=url)
        except Exception:
            return response(500)


class mkdir(Resource):
    def post(self, bucket_name):
        try:
            bucket.mkdir(get_resources(), bucket_name, request.form["directory"])
            return response(201)
        except Exception:
            return response(500)


class gmt(Resource):
    def get(self):
        try:
            msg = []
            policies = bucket_gmt.get_policies()

            for zone in policies:
                policy_id, description, _ = policies[zone].values()
                if not description:
                    description = "No description"
                msg.append({"Name": zone, "Id": policy_id, "Description": description})
            return response(200, data=msg)
        except Exception:
            return response(500)
