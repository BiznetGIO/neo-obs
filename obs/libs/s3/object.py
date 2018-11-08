from obs.libs.s3 import login as login_lib
from obs.libs.utils import log_utils


def list_object(session=None, bucket=None):
    if not session:
        session = login_lib.get_client_session()

    list_object = session.list_objects(Bucket=bucket)
    
    try:
        return list_object.get('Contents')
    except Exception as e:
        log_utils.log_err(e)
        exit()
