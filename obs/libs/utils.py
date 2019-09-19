import sys


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
