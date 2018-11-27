from obs.libs.cloudian import user, qos, credential, bppolicy, usage, permission, group
from obs.libs.s3 import login, bucket, object

list_group = group.group_list()
print(list_group)
exit()

# get user list
list_user_params = {
    'groupId': 'testing',
    'userType': 'all',
    'userStatus': 'active'
}
# list_user = user.get_list(data=list_user_params)
# print(list_user)

# get user detail
detail_user_param = {
    'userId': 'buatdarilib1',
    "groupId": "testing"
}
# detail_user = user.detail(data=detail_user_param)
# print(detail_user)

# create user
create_user_param = {
    "address1": "456 Shakedown St.",
    "city": "Portsmouth",
    "zip": "03803",
    "phone": "132-132-1312",
    "website": "",
    "active": "true",
    "userType": "User",
    "emailAddr": "jgarc@geemail.com",
    "fullName": "Jerry Garcia",
    "groupId": "testing",
    "userId": "neoobs5",
    "state": "NH",
    "country": "USA"
}
# create_user = user.create(data=None, json=create_user_param, method='PUT')
# print(create_user)

# update user
update_user_param = {
    "address1": "456 Shakedown St.",
    "city": "update 3",
    "zip": "03803",
    "phone": "132-132-1312",
    "website": "",
    "active": "true",
    "userType": "User",
    "emailAddr": "jgarc@geemail.com",
    "fullName": "Jerry Garcia",
    "groupId": "testing",
    "userId": "neoobs2",
    "state": "NH",
    "country": "USA"
}
# update_user = user.update(data=None, json=update_user_param)
# print(update_user)

# delete user
delete_user_param = {
    'userId': 'neoobs1',
    'groupId': 'testing'
}
# delete_user = user.delete(data=delete_user_param)
# print(delete_user)

# list qos
list_qos = {
    'userId': 'user_483_20973_stage_wjv-1',
    'groupId': 'testing'
}
# list_qos = qos.get(data=list_qos)
# print(list_qos)

# update qos
update_qos = {
    'userId': 'user_483_20973_stage_wjv-1',
    'groupId': 'testing',
    'storageQuotaKBytes': 20*1024*1024,
    'storageQuotaCount': -1,
    'wlRequestRate': 10,
    'hlRequestRate': 20,
    'wlDataKBytesIn': -1,
    'hlDataKBytesIn': -1,
    'wlDataKBytesOut': -1,
    'hlDataKBytesOut': -1
}
# update_qos = qos.update(data=update_qos)
# print(update_qos)

# delete qos
delete_qos = {
    'userId': 'neoobs5',
    'groupId': 'testing',
}
delete_qos = qos.delete(data=delete_qos)
print(delete_qos)


# get detail credential
detail_credential_params = {
    'accessKey': '5d2579675d04646cf5f4'
}
# detail_credential = credential.get_credential(data=detail_credential_params)
# print(detail_credential)


# get list credential
list_credential_params = {
    'userId': 'buatdarilib1',
    'groupId': 'testing',
}
# list_credential = credential.get_credential(data=list_credential_params)
# print(list_credential)

# get list active credential
list_active_credential_params = {
    'userId': 'buatdarilib1',
    'groupId': 'testing',
    'active': True
}
# list_active_credential = credential.get_credential(data=list_active_credential_params)
# print(list_active_credential)

# post user credential
post_user_params = {
    'userId': 'buatdarilib1',
    'groupId': 'testing',
    'accessKey': 'desiredaccesskey',
    'secretKey': 'desiredsecretkey'
}
# post_user_credential = credential.create(data=post_user_params, method='POST')
# print(post_user_credential)

# put user credential
put_user_params = {
    'userId': 'buatdarilib1',
    'groupId': 'testing'
}
# post_user_credential = credential.create(data=post_user_params, method='PUT')
# print(post_user_credential)


# get list policy
# list_policy = bppolicy.get_policy()
# print(list_policy)

# user_483_20973_stage_wjv-1
# get policy
policy_params = {
    'policyId': '9f934425b7f5de611c32d6320be45c59'
}
# policy = bppolicy.get_policy(data=policy_params)
# print(policy)

# list bucket in policy
# bucket = bppolicy.buckets_policy()
# print(bucket)

# get usage data
usage_data_params = {
    'id': 'testing|buatdarilib1',
    'operation': 'SB',
    'startTime': '',
    'endTime': '',
    'granularity': 'day',
    'reversed': False
}
# usage_data = usage.get_usage(data=usage_data_params)
# print(usage_data)


# get permission
permission_params = {
    'userId': '',
    'groupId': '',
    'bucketName': '',
    'objectName': ''
}
# permission_data = permission.get_permission(data=permission_params)
# print(permission_data)

create_permission_params = {
    'expiryTime': '',
    'allowRead': '',
    'maxDownloadNum': '',
    'secure': '',
    'url': ''
}
# create_permission_data = permission.create_permission(data=permission_params, json=create_permission_params)
# print(create_permission_data)


## S3

# login_data = login.generate_session(access_key='5205dc2b8924f5306283', secret_key='F2Q4Aho1uoIaY4GVwwMgQXrj7Gq0HikxBtueTqAM')
# print(login_data)

# print(login.get_client_session())
# print(login_data)
# print(bucket.list_bucket())

# print(login.get_session())
# bucket_list = bucket.bucket_list()
# print(bucket_list)

# create_bucket = bucket.post_bucket(name='bucketsatu')
# print(create_bucket)

# print(login.test_login(access_key='aabbcc', secret_key='qqwweerrttyy'))
json = {
    'acl': 'public-read',
    'acp': {
        'Grants': [
            {
                'Grantee': {
                    'DisplayName': 'string',
                    'EmailAddress': 'string',
                    'ID': 'string',
                    'Type': 'Group',
                    'URI': 'string'
                },
                'Permission': 'FULL_CONTROL'
            }
        ],
        'Owner': {
            'DisplayName': 'string',
            'ID': 'string'
        }
    }
}
# print(bucket.put_bucket_acl(name='create4', aclParams=json))


# list_bucket = bucket.bucket_list()
# print(list_bucket)
# print(bucket.delete_bucket(name='create_bucket_semua_satu2'))



# create_object = object.put_object(bucket='bucketdua', key='/Users/ramadhanrezza/Desktop/Screen Shot 2018-11-02 at 10.26.40.png')
# print(create_object)

# object_list = object.list_object(bucket='bucketdua')
# print(object_list)


# object_detail = object.get_object(bucket='bucketdua', key='Screen Shot 2018-11-02 at 10.26.40.png')
# print(object_detail)

# object_upload = object.put_object_multipart(bucket='bucketdua', key='/Users/ramadhanrezza/Desktop/Screen Shot 2018-11-02 at 10.26.40.png')
# print(object_upload)
