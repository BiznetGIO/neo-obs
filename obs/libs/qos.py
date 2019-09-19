def info(client, user_id, group_id):
    """Get QoS info of specified user"""
    qos = client.qos.limits(method="GET", userId=user_id, groupId=group_id)
    return qos


def set(client, user_id, group_id, limit):
    """Set QoS of specified user"""
    qos = client.qos.limits(
        method="POST",
        userId=user_id,
        groupId=group_id,
        storageQuotaKBytes=limit,
        storageQuotaCount=-1,
        wlRequestRate=-1,
        hlRequestRate=-1,
        wlDataKBytesIn=-1,
        hlDataKBytesIn=-1,
        wlDataKBytesOut=-1,
        hlDataKBytesOut=-1,
    )
    return qos


def rm(client, user_id, group_id):
    """Remove QoS of specified user"""
    qos = client.qos.limits(method="DELETE", userId=user_id, groupId=group_id)
    return qos
