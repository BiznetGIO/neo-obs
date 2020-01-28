import bitmath
import obs.libs.user as user
import obs.libs.credential as credential
import obs.libs.qos as qos
import obs.cli.admin.qos as qos_limit
import obs.libs.auth as client

from distutils.util import strtobool
from app.helpers.rest import response
from flask import request, jsonify
from flask_restful import Resource, reqparse


def get_client():
    return client.admin_client()


class user_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_type", type=str)
        parser.add_argument("user_status", type=str)
        parser.add_argument("limit", type=str)
        parser.add_argument("userId", type=str)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            if args["userId"]:
                users = user.info(get_client(), args["userId"], args["groupId"])
                if "reason" in users:
                    return response(users["status_code"], message=users["reason"])
                return response(200, data=users)

            user_type = args["user_type"] if args["user_type"] else "all"
            user_status = args["user_status"] if args["user_status"] else "active"
            limit = args["limit"] if args["limit"] else ""

            list = user.list_user(
                get_client(), args["groupId"], user_type, user_status, limit
            )
            if "reason" in list:
                return response(list["status_code"], message=list["reason"])

            return response(200, data=list)
        except Exception:
            return response(500)

    def post(self):
        options = {
            "userId": "",
            "groupId": "",
            "userType": "User",
            "fullName": "",
            "emailAddr": "",
            "address1": "",
            "city": "",
            "state": "",
            "zip": "",
            "country": "",
            "phone": "",
            "website": "",
            "active": True,
            "ldapEnabled": False,
        }

        parser = reqparse.RequestParser()
        for index, option in options.items():
            parser.add_argument(index, type=str, help=f"input user {index}")
        parser.add_argument("quotaLimit", type=int)
        args = parser.parse_args()

        try:
            for index, option in options.items():
                if args[index] not in (option, None):
                    options[index] = args[index]
            status = user.create(get_client(), options)
            if args["quotaLimit"]:
                status=qos.set(get_client(), args["userId"], args["groupId"], args["quotaLimit"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])
            else:
                return response(201, data=status)
        except Exception:
            return response(500)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        parser.add_argument("suspend", type=str, required=True)
        args = parser.parse_args()
        
        try:
            msg='suspended' if args['suspend']=='true' else 'unsuspended'

            users = user.info(get_client(), args["userId"], args["groupId"])
            if users['active']==f"{not strtobool(args['suspend'])}".lower():
                return response(400,f"User already {msg}")   

            del users["canonicalUserId"]
            users["active"]=(not strtobool(args['suspend']))
            status=user.update(get_client(),users)
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            message=f"User has been {msg}"
            return response(200,message)
        except Exception:
            response(500)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str)
        parser.add_argument("groupId", type=str)
        args = parser.parse_args()

        try:
            status = user.remove(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception:
            return response(500)


class qos_api(Resource):
    def get(self, groupId, userId):
        try:
            infos = qos.info(get_client(), userId, groupId)
            infos["Storage Limit"] = str(qos_limit.get_limit_kbytes(infos))
            if "reason" in infos:
                return response(infos["status_code"], message=infos["reason"])

            return response(200, data=infos)
        except Exception:
            return response(500)

    def post(self, groupId, userId):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int)
        args = parser.parse_args()

        try:
            status = qos.set(get_client(), userId, groupId, args["limit"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(201)
        except Exception:
            return response(500)

    def delete(self, groupId, userId):
        try:
            status = qos.rm(get_client(), userId, groupId)
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception:
            return response(500)


class cred_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str)
        parser.add_argument("groupId", type=str)
        args = parser.parse_args()

        try:
            list = credential.list(get_client(), args["userId"], args["groupId"])
            if "reason" in list:
                return response(list["status_code"], message=list["reason"])

            return response(200, data=list)
        except Exception:
            return response(500)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str)
        parser.add_argument("groupId", type=str)
        args = parser.parse_args()

        try:
            status = credential.create(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(201)
        except Exception:
            return response(500)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str)
        parser.add_argument("status", type=str)
        args = parser.parse_args()

        try:
            status = credential.status(get_client(), args["access_key"], args["status"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception:
            return response(500)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str)
        args = parser.parse_args()

        try:
            status = credential.rm(get_client(), args["access_key"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception:
            return response(500)
