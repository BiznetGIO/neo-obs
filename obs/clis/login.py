from obs.clis.base import Base
from obs.libs.utils import log_utils
from obs.libs.utils import env_utils


class Login(Base):
    """
    Usage:
    login cloudian
    login cloudian [-u URL] [-p PORT]
    login s3
    login s3 [-u URL] [-a ACCESSKEY] [-s SECRETKEY]

    """

    default_port_cloudian = 19443
    default_url_cloudian = "http://103.77.104.76"

    def execute(self):
        if self.args["cloudian"]:
            if not env_utils.check_env("cloudian"):
                log_utils.log_warn("No Env Found")
                question = log_utils.question("Create Env? ")
                if question:
                    username = log_utils.get_log("Username : ")
                    password = log_utils.get_pass("pass : ")
                    env_utils.create_env_file_cloudian(
                        username=username,
                        password=password,
                        port=self.default_port_cloudian,
                        url=self.default_url_cloudian,
                    )
                else:
                    exit()

        if self.args["s3"]:
            if not env_utils.check_env("s3"):
                log_utils.log_warn("No Env Found")
                question = log_utils.question("Create Env? ")
                if question:
                    endpoint = log_utils.get_log("Endpoint URL: ")
                    access_key = log_utils.get_log("Access Key: ")
                    secret_key = log_utils.get_log("Secret Key: ")
                    env_utils.create_env_file_s3(
                        endpoint=endpoint, access_key=access_key, secret_key=secret_key
                    )
                else:
                    exit()
