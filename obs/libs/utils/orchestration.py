import os

from obs.libs.utils import cli_utils, log_utils, yaml_utils
from obs.libs.cloudian import user, credential


def check_manifest_file():
    obs_file = None
    cwd = os.getcwd()
    if os.path.exists("{}/obs.yaml".format(cwd)):
        obs_file = "{}/obs.yaml".format(cwd)
    if os.path.exists("{}/obs.yml".format(cwd)):
        obs_file = "{}/obs.yml".format(cwd)
    return obs_file


def do_create(initialize):
    try:
        create_data = {}
        stack = list(initialize.keys())[0]
        stack_name = list(initialize[stack])[0]
        if stack == 'cloudian':
            if initialize[stack][stack_name]['template'] == 'user':
                parameters = initialize[stack][stack_name]['parameters']
                create_data = user.create(data=None, json=parameters)
            
            if initialize[stack][stack_name]['template'] == 'credentials':
                parameters = initialize[stack][stack_name]['parameters']
                method = 'POST'
                if 'accessKey' not in parameters:
                    method = 'PUT'

                create_data = credential.create(data=parameters, json=None, method=method)

        return create_data

    except Exception as e:
        log_utils.log_err(e)
        raise
    else:
        pass
    finally:
        pass
        