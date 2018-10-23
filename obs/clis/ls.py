from obs.clis.base import Base
from obs.libs.cloudian import user, qos, credential
from obs.libs.utils import log_utils
from tabulate import tabulate


class Ls(Base):
    """
    Usage:
    ls user [-g GROUP_ID] [-i ID]
    ls user
    ls qos [-g GROUP_ID] [-i ID]
    ls credential [-g GROUP_ID] [-i ID]

    Options:
    -h --help                             Print usage
    -g GROUP_ID --group_id=GROUP_ID       Set obs Group Id
    -i ID --id=ID                         Set obs User Id

    """
    def execute(self):
        if self.args['user']:
            if self.args['--group_id'] and self.args['--id']:
                tab_data = list()
                data = {
                    "groupId": self.args['--group_id'],
                    "userId": self.args['--id'],
                }
                result = user.get(data=data)

                try:
                    user_data = user.get(data=data)['data']
                except Exception as e:
                    log_utils.log_err(result['status_message'])
                else:
                    user_data_fix = {
                        "UserType": user_data['userType'],
                        "Name": user_data['fullName'],
                        "EmailAddr": user_data['emailAddr'],
                        "Address": user_data['address1']+user_data['address2'],
                        "City": user_data['city'],
                        "Status": user_data['active']
                    }
                    tab_data.append(user_data_fix)
                    print(tabulate(tab_data, headers="keys", tablefmt="grid"))
            else:
                data = {
                    "groupId": "testing",
                    "userType": "all",
                    "userStatus": "active"
                }
                data_user = list()
                all_user = user.list(data=data)
                number = 1
                for items in all_user['data']:
                    data_item = {
                        "No.": number,
                        "User": items['userId'],
                        "Name": items['fullName'],
                        "EmailAddr": items['emailAddr'],
                        "Address": items['address1'],
                        "City": items['city'],
                        "Status": items['active']
                    }
                    number = number+1
                    data_user.append(data_item)

                print(
                    tabulate(
                        data_user,
                        headers="keys",
                        tablefmt="grid"
                    )
                )

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
                        "User": qos_data['userId'],
                        "Quota": "{} GB".format(quota/1024**2)
                    }
                    tab_data.append(user_qos)
                    print(tabulate(tab_data, headers="keys", tablefmt="grid"))
                    exit()
            else:
                log_utils.log_err('Missing parameter.')
                exit()

        if self.args['credential']:
            if self.args['--group_id'] and self.args['--id']:
                pass
            else:
                log_utils.log_err('Missing parameter.')
