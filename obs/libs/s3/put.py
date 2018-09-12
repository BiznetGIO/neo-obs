from obs.libs.s3 import requestors, parser
import os


def do_put(json_data=None):
    resource = parser.get_resource(json_data)
    method = parser.get_method(json_data)

    APP_STATIC = os.path.dirname(__file__)
    parameters = {}
    if json_data[resource][method]['parameters']:
        parameters = parser.parser(json_data, APP_STATIC)

    result = requestors.request(method,parameters)

    return result
