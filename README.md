NEO-OBS
==========

NEO-OBS is python based library for cloudian and s3 usage.


Installing
-----

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/)

NEO OBS only support Python3.

``` bash
pip install neo-obs
```

Usage
-----

```
from obs.client import CloudianClient, S3Client
```

Cloudian Client Example: 
```
obsclient = CloudianClient(
    url="<YOUR-URL-ADDRESS",
    user=<user>,
    password=<pass>,
    port=1000
)


# get list Users
list_params = {
    "groupId": "testing",
    "userType": "all",
    "userStatus": "active"
}
print(obsclient.user.list(data=list_params))


# get detail user
get_params = {
    "userId": "<USERID>",
    "groupId": "testing",
}
print(obsclient.user.get(data=get_params))


# create new user
create_params = {
    "userId": "<USERID>",
    "groupId": "testing",
    "userType": "User"
}
print(obsclient.user.create(data=None, json=create_params, method="PUT"))