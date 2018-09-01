from obs.clis.base import Base
from obs.libs.cloudian import user
from obs.libs.cloudian.requestors import request
from obs.libs.cloudian import qos

class Ls(Base):
    """
    Usage:
    ls user
    ls qos

    """
    def execute(self):
        if self.args['user']:
            print("User")