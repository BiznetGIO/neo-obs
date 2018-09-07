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


Usage Cloudian (User Now)
-----

Login and setup env
``` bash
obs login cloudian
```

now check your env
``` bash
cat ~/.obs/cloudian.env
```

get user identity
``` bash
obs ls user -g your_group_id -i your_id
```

