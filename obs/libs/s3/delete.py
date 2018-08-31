from .requestors import S3Requestor
from .parser import get_resource, get_method, parser

import os


class DeleteStack(object):
    def __init__(self, requestor):
        self.requestor = requestor

    def do_delete(self, json_data=None):
        resource = get_resource(json_data)
        method = get_method(json_data)

        APP_STATIC = os.path.dirname(__file__)
        parameters = {}
        if json_data[resource][method]['parameters']:
            parameters = parser(json_data, APP_STATIC)

        return S3Requestor.call_fn(self.requestor, method, parameters)
