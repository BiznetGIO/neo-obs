from obs.clis.base import Base
from obs.libs.utils import log_utils
from obs.libs.utils import login


class Login(Base):
    """
    Usage:
    login cloudian
    login s3

    """

    def execute(self):
        if self.args['cloudian']:
            username = log_utils.get_log("Username  : ")
            password = log_utils.get_pass("Password : ")
            port = log_utils.get_log("Port: ")

            log_utils.log_info(username)
            log_utils.log_info(password)
            log_utils.log_info(port)
            login.

        if self.args['s3']:
            key = log_utils.get_log("Key : ")
            secret = log_utils.get_pass("Secret : ")
            region = log_utils.get_log("Region : ")
            endpoint = log_utils.get_log("Endpoint : ")

            log_utils.log_info(key)
            log_utils.log_info(secret)
            log_utils.log_info(region)
            log_utils.log_info(endpoint)