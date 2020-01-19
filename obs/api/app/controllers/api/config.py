from obs.libs import config
from app.helpers.rest import response
from flask import request, jsonify
from flask_restful import Resource, reqparse

def open_config():
    data={}
    path=open(config.config_file(),"r")
    for line in path:
        line=line.split("=")
        data[line[0]]=line[1][:-1]
    return data

class config_api(Resource):
    def get(self):
        configure=open_config()
        return response(200,data=configure)

    def put(self):
        configure=open_config()
        parser = reqparse.RequestParser()
        for key in configure.keys():
            parser.add_argument(key, type=str)
        args = parser.parse_args()

        path=open(config.config_file(),"w")
        line=""
        for arg,value in args.items():
            if value is not None:
                configure[arg]=value
        for key,value in configure.items():
            line+=f"{key}={value}\n"

        path.write(line)
        return response(200)