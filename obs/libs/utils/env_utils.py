from dotenv import load_dotenv
import os


home = os.path.expanduser("~")


def check_env():
    return os.path.isfile("{}/.obs.env".format(home))


def create_env_file_cloudian(username, password, port=None, url=None):

    try:
        env_file = open("{}/.neo.env".format(home), "w+")
        env_file.write("OS_USERNAME=%s\n" % username)
        env_file.write("OS_PASSWORD=%s\n" % password)
        env_file.write("OS_AUTH_URL=%s\n" % url)
        env_file.write("OS_PORT=%s\n" % port)
        env_file.close()
        return True
    except:
        return False

def create_env_file_s3(key, secret, region=None, endpoint=None):

    try:
        env_file = open("{}/.neo.env".format(home), "w+")
        env_file.write("OS_KEY=%s\n" % key)
        env_file.write("OS_SECRET=%s\n" % secret)
        env_file.write("OS_REGION=%s\n" % region)
        env_file.write("OS_ENDPOINT=%s\n" % endpoint)
        env_file.close()
        return True
    except:
        return False

def load_env_file():
    return load_dotenv("{}/.obs.env".format(home), override=True)


def get_env_values_cloudian():
    load_env_file()
    obs_env = {}
    obs_env['username'] =  os.environ.get('OS_USERNAME')
    obs_env['password'] = os.environ.get('OS_PASSWORD')
    obs_env['url'] = os.environ.get('OS_AUTH_URL')
    obs_env['port'] = os.environ.get('OS_PORT')
    return obs_env


def get_env_values_s3():
    load_env_file()
    obs_env = {}
    obs_env['key'] =  os.environ.get('OS_KEY')
    obs_env['secret'] = os.environ.get('OS_SECRET')
    obs_env['region'] = os.environ.get('OS_REGION')
    obs_env['endpoint'] = os.environ.get('OS_ENDPOINT')
    return obs_env