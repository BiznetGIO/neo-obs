NEO-OBS
==========

NEO-OBS is python based library for cloudian and s3 usage.


Installing
-----

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/)

NEO OBS only support Python3.

``` bash
pip3 install -U neo-cli
```

Usage
-----

from obs.client import CloudianClient, S3Client

obsclient = CloudianClient(
    url="<YOUR-URL-ADDRESS",
    user=<user>,
    password=<pass>,
    port=1000
)

s3client = S3Client(
    region=<region>,
    endpoint=<s3 endpoint>,
    key=<s3 key>,
    secret=<s3 secret key>
)