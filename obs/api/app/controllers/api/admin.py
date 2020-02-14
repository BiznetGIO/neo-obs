from obs.libs import qos
from obs.libs import user
from obs.libs import credential
from obs.libs import auth as client
from obs.libs import admin as admin_usage
from distutils.util import strtobool
from obs.api.app.helpers.rest import response
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

            user_list = user.list_user(
                get_client(), args["groupId"], user_type, user_status, limit
            )
            if "reason" in user_list:
                return response(list["status_code"], message=list["reason"])

            return response(200, data=user_list)
        except Exception as exc:
            return response(500, str(exc))

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
            if index in ["userId", "groupId", "fullName"]:
                parser.add_argument(index, type=str, required=True)
            parser.add_argument(index, type=str)
        parser.add_argument("quotaLimit", type=int)
        args = parser.parse_args()

        try:
            for index, option in options.items():
                if args[index] not in (option, None):
                    options[index] = args[index]
            status = user.create(get_client(), options)
            if args["quotaLimit"]:
                status = qos.set(
                    get_client(), args["userId"], args["groupId"], args["quotaLimit"]
                )
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])
            else:
                return response(201)
        except Exception as exc:
            return response(500, str(exc))

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        parser.add_argument("suspend", type=str, required=True)
        args = parser.parse_args()

        try:
            msg = "suspended" if args["suspend"] == "true" else "unsuspended"
            users = user.info(get_client(), args["userId"], args["groupId"])
            if users["active"] == f"{not strtobool(args['suspend'])}".lower():
                return response(400, f"User already {msg}")

            # canocicalUserId can't be included when updating user
            del users["canonicalUserId"]
            users["active"] = not strtobool(args["suspend"])
            status = user.update(get_client(), users)
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            message = f"User has been {msg}"
            return response(200, message)
        except Exception as exc:
            response(500, str(exc))

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            status = user.remove(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception as exc:
            return response(500, str(exc))


class qos_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            infos = qos.info(get_client(), args["userId"], args["groupId"])
            infos["Storage Limit"] = (
                infos["qosLimitList"][0]["value"] * 1024
                if infos["qosLimitList"][0]["value"] != -1
                else "unlimited"
            )

            if "reason" in infos:
                return response(infos["status_code"], message=infos["reason"])

            return response(200, data=infos)
        except Exception as exc:
            return response(500, str(exc))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        parser.add_argument("limit", type=int, required=True)
        args = parser.parse_args()

        try:
            status = qos.set(
                get_client(), args["userId"], args["groupId"], args["limit"]
            )
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(201)
        except Exception as exc:
            return response(500, str(exc))

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            status = qos.rm(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception as exc:
            return response(500, str(exc))


class cred_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            cred_list = credential.list(get_client(), args["userId"], args["groupId"])
            if "reason" in cred_list:
                return response(list["status_code"], message=list["reason"])

            return response(200, data=cred_list)
        except Exception as exc:
            return response(500, str(exc))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            status = credential.create(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(201)
        except Exception as exc:
            return response(500, str(exc))

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        parser.add_argument("status", type=str, required=True)
        args = parser.parse_args()

        try:
            status = credential.status(get_client(), args["access_key"], args["status"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception as exc:
            return response(500, str(exc))

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("access_key", type=str, required=True)
        args = parser.parse_args()

        try:
            status = credential.rm(get_client(), args["access_key"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(204)
        except Exception as exc:
            return response(500, str(exc))


class user_usage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=str, required=True)
        parser.add_argument("groupId", type=str, required=True)
        args = parser.parse_args()

        try:
            status = admin_usage.usage(get_client(), args["userId"], args["groupId"])
            if "reason" in status:
                return response(status["status_code"], message=status["reason"])

            return response(200, data=status[0])
        except Exception as exc:
            return response(500, str(exc))
