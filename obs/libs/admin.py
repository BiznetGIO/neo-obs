import datetime


def usage(client, user_id, group_id):
    """Get storage usage."""
    # for `raw` granularity, the interval between
    # "startTime" and "endTime" must not exceed 24 hours.
    now = datetime.datetime.now(datetime.timezone.utc)
    yesterday = now - datetime.timedelta(1)
    du = client.usage(
        id=f"{group_id}|{user_id}",
        operation="SB",
        startTime=f"{yesterday:%Y%m%d}0000",
        endTime=f"{now:%Y%m%d}0000",
        granularity="raw",
    )
    return du
