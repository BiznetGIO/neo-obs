from obs.libs.utils import env_utils
from obs.libs.utils import files_utils
from obs.libs.utils import log_utils
from obs.libs.utils import sess_utils
from obs.libs.utils import vars_utils

from obs.libs.cloudian.user import User
from obs.libs.cloudian.qos import Qos
from obs.libs.cloudian.bppolicy import BucketPolicy

from obs.libs.s3.bucket import Bucket
from obs.libs.s3.put import PutStack
from obs.libs.s3.get import GetStack
from obs.libs.s3.delete import DeleteStack

from obs.libs.cloudian.requestors import CloudianRequestor
from obs.libs.s3.requestors import S3Requestor


def do_login(key=None, secret=None, reg=None, endp=None, action=None):
    """
    s3  | cloudian

    key | username
    secret | password
    endpoint | url
    region | port

    """
    if action == 'cloudian':



def do_logout():
    pass