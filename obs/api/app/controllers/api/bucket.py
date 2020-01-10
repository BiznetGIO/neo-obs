import bitmath
import obs.libs.gmt as bucket_gmt
import obs.libs.bucket as bucket
import obs.libs.auth as resource

from app.helpers.rest import response
from flask import request, jsonify
from flask_restful import Resource, reqparse


def get_resources():
    return resource.resource()


def get_plain_auth():
    return resource.plain_auth()


class list(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bucket_name", type=str)
        args = parser.parse_args()

        if args["bucket_name"]:
            buckets = bucket.get_objects(
                get_resources(), bucket_name=args["bucket_name"]
            )
            all_bucket = []
            for index, obj in enumerate(buckets):
                all_bucket.append(
                    {
                        "key": obj.key,
                        "size": obj.size,
                        "modified": f"{obj.last_modified:%Y-%m-%d %H:%M:%S}",
                    }
                )
            return jsonify(all_bucket)

        buckets = bucket.buckets(get_resources())
        all_bucket = []
        for index, buck in enumerate(buckets):
            all_bucket.append({"name": buck.name, "creation_date": buck.creation_date})
        return jsonify(all_bucket)


class bucket_api(Resource):
    def get(self, bucket_name):
        bucket_info = bucket.bucket_info(get_resources(), bucket_name, get_plain_auth())
        return jsonify(bucket_info)

    def post(self, bucket_name):
        bucket.create_bucket(auth=get_plain_auth(), bucket_name=bucket_name)
        return response(201)

    def delete(self, bucket_name):
        bucket.remove_bucket(get_resources(), bucket_name)
        return response(204)


class object_api(Resource):
    def get(self, bucket_name, object_name):
        object_info = bucket.object_info(get_resources(), bucket_name, object_name)
        return jsonify(object_info)

    def post(self, bucket_name, object_name, basename=None):
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str)
        parser.add_argument("use_basename", type=str)
        args = parser.parse_args()

        if args["use_basename"]:
            basename = True

        bucket.upload_object(
            resource=get_resources(),
            bucket_name=bucket_name,
            path=object_name,
            object_name=args["file_name"],
            use_basename=basename,
        )

        return response(201)

    def delete(self, bucket_name, object_name):
        bucket.remove_object(get_resources(), bucket_name, object_name)
        return response(204)


class move_object(Resource):
    def post(self, bucket_name, object_name):
        bucket.move_object(
            get_resources(), bucket_name, request.form["move_to"], object_name
        )
        return response(204)


class copy_object(Resource):
    def post(self, bucket_name, object_name):
        bucket.copy_object(
            get_resources(), bucket_name, request.form["copy_to"], object_name
        )
        return response(204)


class download_object(Resource):
    def get(self, bucket_name, object_name):
        bucket.download_object(get_resources(), bucket_name, object_name)
        return response(204)


class usage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        args = parser.parse_args()

        if args["name"]:
            total_size, total_objects = bucket.bucket_usage(
                get_resources(), args["name"]
            )
            return jsonify(
                {"name": args["name"], "size": total_size, "objects": total_objects}
            )

        disk_usage = {"bucket": [], "total_usage": 0}
        disk_usages = bucket.disk_usage(get_resources())
        for usage in disk_usages:
            bucket_name = usage[0]
            total_size, total_objects = usage[1]
            disk_usage["total_usage"] += total_size
            disk_usage["bucket"].append(
                {"name": bucket_name, "size": total_size, "objects": total_objects}
            )

        return jsonify(disk_usage)


class acl(Resource):
    def post(self, acl_type="bucket", acl="private"):
        parser = reqparse.RequestParser()
        parser.add_argument("bucket_name", type=str, required=True)
        parser.add_argument("object_name", type=str)
        parser.add_argument("acl", type=str)
        args = parser.parse_args()

        if args["object_name"]:
            acl_type = "object"

        if args["acl"]:
            acl = args["acl"]

        bucket.set_acl(
            resource=get_resources(),
            bucket_name=args["bucket_name"],
            object_name=args["object_name"],
            acl_type=acl_type,
            acl=acl,
        )

        return response(204)


class presign(Resource):
    def get(self, bucket_name, object_name):
        parser = reqparse.RequestParser()
        parser.add_argument("expire", type=int)
        args = parser.parse_args()

        url = bucket.generate_url(
            get_resources(), bucket_name, object_name, args["expire"]
        )
        return jsonify({"url": url})


class mkdir(Resource):
    def post(self, bucket_name):
        bucket.mkdir(get_resources(), bucket_name, request.form["directory"])
        return response(201)


class gmt(Resource):
    def get(self):
        msg = []
        policies = bucket_gmt.get_policies()

        for zone in policies:
            policy_id, description, _ = policies[zone].values()
            if not description:
                description = "No description"
            msg.append({"Name": zone, "Id": policy_id, "Description": description})
        return jsonify(msg)
