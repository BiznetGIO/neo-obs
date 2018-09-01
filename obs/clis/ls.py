from obs.clis.base import Base
from obs.libs.cloudian import user
from obs.libs.utils import log_utils
from tabulate import tabulate

class Ls(Base):
    """
    Usage:
    ls user [-g GROUP_ID] [-i ID]
    ls user
    ls qos

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
                user_data = user.get(data=data)['data']
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
                all_user = user.list(data=data)
                log_utils.log_info(all_user)
