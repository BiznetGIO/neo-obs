from obs.clis.base import Base
from obs.libs.cloudian import user, qos, credential
from obs.libs.s3 import bucket, object
from obs.libs.utils import log_utils
from tabulate import tabulate

import time


class Ls(Base):
    '''
    Usage:
    ls user [-g GROUP_ID] [-i ID]
    ls user
    ls qos [-g GROUP_ID] [-i ID]
    ls credential [-g GROUP_ID] [-i ID]
    ls credential [-g GROUP_ID] [-i ID] [-s STATUS]
    ls credential [-k KEY]
    ls bucket
    ls object [-b bucket]

    Options:
    -h --help                             Print usage
    -g GROUP_ID --group_id=GROUP_ID       Set obs Group Id
    -i ID --id=ID                         Set obs User Id
    -k KEY --key=KEY                      Set obs Secret Key
    -s STATUS --status=STATUS
    -b BUCKET --bucket=BUCKET

    '''
    def execute(self):
        if self.args['user']:
            if self.args['--group_id'] and self.args['--id']:
                tab_data = list()
                data = {
                    'groupId': self.args['--group_id'],
                    'userId': self.args['--id'],
                }
                user_data = user.detail(data=data)
                if user_data is None:
                    log_utils.log_err(user_data)
                    exit()
                else:
                    user_data_fix = {
                        'UserType': user_data['userType'],
                        'Name': user_data['fullName'],
                        'EmailAddr': user_data['emailAddr'],
                        'Address': user_data['address1']+user_data['address2'],
                        'City': user_data['city'],
                        'Status': user_data['active']
                    }
                    tab_data.append(user_data_fix)
                    print(tabulate(tab_data, headers='keys', tablefmt='grid'))
            else:
                data = {
                    'groupId': 'testing',
                    'userType': 'all',
                    'userStatus': 'active'
                }
                data_user = list()
                all_user = user.get_list(data=data)
                number = 1
                for items in all_user:
                    data_item = {
                        'No.': number,
                        'User': items['userId'],
                        'Name': items['fullName'],
                        'EmailAddr': items['emailAddr'],
                        'Address': items['address1'],
                        'City': items['city'],
                        'Status': items['active']
                    }
                    number = number+1
                    data_user.append(data_item)

                print(tabulate(data_user, headers='keys', tablefmt='grid'))

        if self.args['qos']:
            if self.args['--group_id'] and self.args['--id']:
                tab_data = list()
                list_params = {
                    'userId': self.args['--id'],
                    'groupId': self.args['--group_id']
                }

                try:
                    qos_data = qos.get(data=list_params)
                    limitList = qos_data['qosLimitList']
                except Exception as e:
                    log_utils.log_err(e)
                    exit()
                else:
                    quota = 0
                    for i in limitList:
                        if i['type'] == 'STORAGE_QUOTA_KBYTES':
                            quota = i['value']

                    user_qos = {
                        'User': qos_data['userId'],
                        'Quota': '{} GB'.format(quota/1024**2)
                    }
                    tab_data.append(user_qos)
                    print(tabulate(tab_data, headers='keys', tablefmt='grid'))
                    exit()
            else:
                log_utils.log_err('Missing parameter.')
                exit()

        if self.args['credential']:
            if self.args['--group_id'] and self.args['--id']:
                list_params = {
                    'userId': self.args['--id'],
                    'groupId': self.args['--group_id']
                }

                credential_list = credential.get_credential(data=list_params)
                if credential_list is None:
                    log_utils.log_err(credential_list)
                    exit()
                else:
                    number = 1
                    data_credential = list()
                    for item in credential_list:
                        cTime = time.strftime("%d-%m-%Y, %H:%M:%S", time.localtime(int(str(item['createDate'])[:-3])))

                        if item['expireDate'] is not None:
                            dTime = time.strftime("%d-%m-%Y, %H:%M:%S", time.localtime(int(str(item['expireDate'])[:-3])))
                        else:
                            dTime = item['expireDate']

                        data_item = {
                            'No.': number,
                            'Access Key': item['accessKey'],
                            'Secret Key': item['secretKey'],
                            'Create': cTime,
                            'Expire': dTime,
                            'Status': item['active']
                        }
                        number = number+1
                        data_credential.append(data_item)

                    print(tabulate(data_credential, headers='keys', tablefmt='grid'))
                    exit()

            elif self.args['--key']:
                tab_data = list()
                list_params = {
                    'accessKey': self.args['--key']
                }
                credential_data = credential.get_credential(data=list_params)

                if credential_data is None:
                    log_utils.log_err(credential_list)
                    exit()
                else:                                                                                                                                                                                                                                                            
                    cTime = time.strftime("%d-%m-%Y, %H:%M:%S",time.localtime(int(str(credential_data['createDate'])[:-3])))
                    if credential_data['expireDate'] is not None:
                        dTime = time.strftime("%d-%m-%Y, %H:%M:%deaS", time.localtime(int(str(credential_data['expireDate'])[:-3])))
                    else:
                        dTime = credential_data['expireDate']

                    cred_detail = {
                        'Access Key': credential_data['accessKey'],
                        'Secret Key': credential_data['secretKey'],
                        'Create': cTime,
                        'Expire': dTime,
                        'Status': credential_data['active']
                    }
                    tab_data.append(cred_detail)
                    print(tabulate(tab_data, headers='keys', tablefmt='grid'))
                    exit()

            else:
                log_utils.log_err('Missing parameter.')
                exit()

        if self.args['bucket']:
            print(bucket.bucket_list())

        if self.args['object']:
            if self.args['--bucket']:
                print(object.list_object(bucket=self.args['--bucket']))
            else:
                log_utils.log_err('Missing parameter.')
                exit()