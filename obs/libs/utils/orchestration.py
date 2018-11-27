import os

def check_manifest_file():
    obs_file = None
    cwd = os.getcwd()
    if os.path.exists("{}/obs.yaml".format(cwd)):
        obs_file = "{}/obs.yaml".format(cwd)
    if os.path.exists("{}/obs.yml".format(cwd)):
        obs_file = "{}/obs.yml".format(cwd)
    return obs_file