from obs.libs.s3 import requestors, parser as ps
import os



def do_get(self, json_data=None):
    resource = ps.get_resource(json_data)
    method = ps.get_method(json_data)

    APP_STATIC = os.path.dirname(__file__)
    parameters = {}
    if json_data[resource][method]['parameters']:
        parameters = ps.parser(json_data, APP_STATIC)

    return requestors.request(method, parameters)
