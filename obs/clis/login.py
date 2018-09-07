from obs.clis.base import Base
from obs.libs.utils import log_utils
from obs.libs.utils import env_utils

class Login(Base):
    """
    Usage:
    login cloudian
    login cloudian [-u URL] [-p PORT]
    login s3

    """
    default_port_cloudian = 19443
    default_url_cloudian = "http://103.77.104.76"

    def execute(self):
        if self.args['cloudian']:
            if not env_utils.check_env('cloudian') :
                log_utils.log_warn("No Env Found")
                question = log_utils.question("Create Env? ")
                if question :
                    username = log_utils.get_log("Username : ")
                    password = log_utils.get_pass("pass : ")
                    env_utils.create_env_file_cloudian(
                        username=username,
                        password=password,
                        port= self.default_port_cloudian,
                        url= self.default_url_cloudian
                    )
                else:
                    exit()
            # env_data = env_utils.get_env_values_cloudian()
            # try:
            #     url = env_data['root_url']
            #     port = env_data['port']
            # except Exception as e:
            #     url = self.default_url
            #     port = self.default_port

        if self.args['s3']:
            print(env_utils.check_env('s3'))
            key = log_utils.get_log("Key : ")
            secret = log_utils.get_pass("Secret : ")
            region = log_utils.get_log("Region : ")
            endpoint = log_utils.get_log("Endpoint : ")

            log_utils.log_info(key)
            log_utils.log_info(secret)
            log_utils.log_info(region)
            log_utils.log_info(endpoint)