from obs.libs.utils import log_utils as log
import dill
import os


def set_session(sess):
    try:
        with open("/tmp/obs-session.pkl", "wb") as f:
            dill.dump(sess, f)
    except Exception as e:
        log.log_err("set session failed")


def get_session():
    try:
        sess = None
        with open("/tmp/obs-session.pkl", "rb") as f:
            sess = dill.load(f)
        return sess
    except Exception as e:
        return False


def check_session():
    return os.path.isfile("/tmp/obs-session.pkl")
