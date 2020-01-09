import bitmath
import obs.libs.user as user
import obs.libs.credential as credential
import obs.libs.qos as qos
import obs.cli.admin.qos as qos_limit
import obs.libs.auth as client

from app.helpers.rest import response
from flask import request, jsonify
from flask_restful import Resource, reqparse

def get_client():
    return client.admin_client()

class user_api(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_type',type=str)
        parser.add_argument('user_status',type=str)
        parser.add_argument('limit',type=str)
        parser.add_argument('userId',type=str)
        parser.add_argument('groupId',type=str,required=True)
        args=parser.parse_args()

        try:
            if args['userId']:
                users=user.info(get_client(),args['userId'],args['groupId'])
                return response(200,data=users)

            user_type=args['user_type'] if args['user_type'] else 'all'
            user_status=args['user_status'] if args['user_status'] else 'active'
            limit=args['limit'] if args['limit'] else ''
            
            list=user.list_user(get_client(),args['groupId'],user_type,user_status,limit)

            return response(200,data=list)
        except Exception:
            return response(500)
        
    def post(self):
        options={
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
        "ldapEnabled": False
        }

        parser=reqparse.RequestParser()
        for index,option in options.items():
            parser.add_argument(index,type=str,help=f"input user {index}")
        args=parser.parse_args()

        try:
            for index,option in options.items():
                if args[index] not in (option,None):
                    options[index]=args[index]
            user.create(get_client(),options)
            return response(201)
        except Exception:
            return response(500)

    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',type=str)
        parser.add_argument('groupId',type=str)
        args=parser.parse_args()

        try:
            user.remove(get_client(),args['userId'],args['groupId'])
            return response(204)
        except Exception:
            return response(500)

class qos_api(Resource):
    def get(self,groupId,userId):
        infos=qos.info(get_client(),userId,groupId)
        infos["Storage Limit"]=str(qos_limit.get_limit_kbytes(infos))
        return jsonify(infos)

    def post(self,groupId,userId):
        qos.set(get_client(),userId,groupId,request.form['limit'])
        return "Success"

    def delete(self,groupId,userId):
        qos.rm(get_client(),userId,groupId)
        return "Success"

class cred_api(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',type=str)
        parser.add_argument('groupId',type=str)
        args=parser.parse_args()

        lists=credential.list(get_client(),args['userId'],args["groupId"])
        return jsonify(lists)

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',type=str)
        parser.add_argument('groupId',type=str)
        args=parser.parse_args()

        credential.create(get_client(),args["userId"],args["groupId"])
        return "Success"

    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('access_key',type=str)
        parser.add_argument('status',type=str)
        args=parser.parse_args()

        credential.status(get_client(),args["access_key"],args["status"])
        return "Success"

    def delete(self):
        credential.rm(get_client(),request.form["access_key"])
        return "Success"