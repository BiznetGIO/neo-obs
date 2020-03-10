from flask import Blueprint
from flask_restful import Api
from .storage import *
from .admin import *

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint)

api.add_resource(bucket_api, "/storage/bucket/<bucket_name>")
api.add_resource(object_api, "/storage/object/<bucket_name>")
api.add_resource(download_object, "/storage/object/download/<bucket_name>")
api.add_resource(upload_object, "/storage/object/upload/<bucket_name>")
api.add_resource(move_object, "/storage/object/move/<bucket_name>")
api.add_resource(copy_object, "/storage/object/copy/<bucket_name>")
api.add_resource(presign, "/storage/presign/<bucket_name>/<object_name>")
api.add_resource(mkdir, "/storage/mkdir/<bucket_name>")
api.add_resource(acl, "/storage/acl")
api.add_resource(list, "/storage/list")
api.add_resource(usage, "/storage/usage")
api.add_resource(gmt_policy, "/storage/gmt")

api.add_resource(user_api, "/admin/user")
api.add_resource(qos_api, "/admin/qos")
api.add_resource(cred_api, "/admin/cred")
api.add_resource(user_usage, "/admin/usage")
