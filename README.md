# NEO-OBS

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

NEO-OBS is python based library for cloudian and s3 usage.

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/)

NEO OBS only support Python3.

``` bash
pip install neo-obs
```

## Usage Cloudian (User Now)

Login and setup env

``` bash
obs login cloudian
```

Now check your env

``` bash
cat ~/.obs/cloudian.env
```

Get user identity

``` bash
obs ls user -g your_group_id -i your_id
```

## Using neo-obs as a library

``` bash
from obs.libs.cloudian import requestors
from obs.libs.cloudian import user

list_params = {
    "groupId": "testing",
    "userType": "all",
    "userStatus": "active"
}
list_user = user.list(data=list_params)
print(list_user)

list_params = {
    "groupId": "testing",
    "userId": "user_264_18957_stage_t2m1",
}
get_user = user.get(data=list_params)
print(get_user)

create_params = {
    "userId": "<USERID>",
    "groupId": "testing",
    "userType": "User"
}
create_user = user.get(data=None, json=create_params)
```


