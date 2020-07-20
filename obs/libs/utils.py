import os
import sys
import tzlocal
import xmltodict
from datetime import datetime
from distutils.util import strtobool


def get_bucket_key(uri):
    """Return bucket name and key from given S3 URI"""
    if uri.startswith("s3://"):
        uri = uri[5:]

    components = uri.split("/")
    bucket = components[0]
    key = ""
    if len(components) > 1:
        key = "/".join(components[1:])
    return bucket, key


def sizeof_fmt(num, suffix="B"):
    """Convert any number to human readable size. By Fred Cirera"""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, "Yi", suffix)


def check(response):
    """Check if response contains error result
    then raise exception."""
    sys.tracebacklimit = 0

    if "reason" in response:
        msg = (
            f"{response.get('reason')} [{response.get('status_code')}]\n"
            f"URL: {response.get('url')}"
        )
        raise ValueError(msg)


def check_plain(response):
    """Check if response contains error result
    then raise exception."""
    if response.text:
        response_dict = xmltodict.parse(response.text)

        if "Error" in response_dict:
            code = response_dict["Error"]["Code"]
            msg = response_dict["Error"]["Message"]
            raise ValueError(f"{code}: {msg}")


def human_date(unixtime):
    """Convert unix timestamp to human readable."""
    # divided by 1000 to convert from miliseconds to seconds
    unix_timestamp = int(unixtime) / 1000
    local_timezone = tzlocal.get_localzone()
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    human_datetime = local_time.strftime("%Y-%m-%d %H:%M:%S%z (%Z)")
    return human_datetime


def compatibility():
    return strtobool(os.environ.get("OBS_USE_NEO"))
