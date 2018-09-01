from obs.clis.base import Base
from obs.libs.utils import log_utils
from obs.libs.utils import env_utils


class Login(Base):
    """
    Usage:
    login cloudian
    login s3

    """
    default_port = 19443
    default_url = "http://103.77.104.76"

    def execute(self):
        if self.args['cloudian']:
            port = self.default_port
            url = self.default_url
            if not env_utils.check_env('cloudian') :
                log_utils("No Env")
                question = log_utils.question("Create Env? ")
                if question :
                    username = log_utils.get_log("Username : ")
                    password = log_utils.get_pass("pass : ")
                    env_utils.create_env_file_cloudian(
                        username="",
                        password="",
                        port=port,
                        url=url
                    )
                else:
                    exit()
            env_data = env_utils.get_env_values_cloudian()
            log_utils.log_info(env_data)

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