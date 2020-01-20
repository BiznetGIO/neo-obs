Storage Usage
=============

.. code-block:: bash

  $ obs storage --help
  Usage: obs storage [OPTIONS] COMMAND [ARGS]...

  Manage user storage.

  Options:
  --help  Show this message and exit.

  Commands:
  acl      Set ACL for bucket or object.
  cp       Copy object to other bucket.
  du       Disk usage of bucket.
  get      Download object in bucket.
  gmt      Manage Cloudian extensions to S3.
  info     Display bucket or object info.
  ls       List bucket or object.
  mb       Create bucket.
  mkdir    Create directory inside bucket
  mv       Move object into other bucket.
  presign  Generate Url for bucket or object.
  put      Upload object to bucket.
  rm       Remove bucket or object.


Every time you want to know available arguments and options for certain command,
don't hesitate to run `--help`

.. code-block:: bash

   $ obs storage mv --help
   Usage: obs storage mv [OPTIONS] [SRC_URI] [DEST_URI]

       Move object into other bucket.

   Options:
       --help  Show this message and exit.

See, I get the help message above which mean, I need to run the command below to
move object

.. code-block:: bash

  $ obs storage mv s3://source-bucket/awesomeobject.png s3://destination-bucket/  



Usage Example
-------------

You can use either `s3://bucket-name` or `bucket-name` directly, both are
accepted.

.. code-block:: bash

  To list all available buckets
  $ obs storage ls

  To list all object inside specific buckets
  $ obs storage ls s3://awesomebucket

  To list all object inside specific "directory"
  $ obs storage ls s3://awesomebucket/foo-dir/

  To remove a bucket
  $ obs storage rm s3://awesomebucket

  To remove object inside bucket
  $ obs storage rm s3://awesomebucket/myobject.png

  To make a bucket
  $ obs storage mb awesomebucket

  To make a bucket suffixed with random string
  $ obs storage mb awesomebucket --random

  To make a bucket with specific ACL
  $ obs storage mb awesomebucket --acl private

  To make a bucket with specific gmt id policy
  $ obs storage mb awesomebucket --policy-id c41e0a6f5e74663bexampleid

  To download an object
  $ obs storage get s3://awesomebucket/myobject.png

  To upload an object with specified name
  $ obs storage put myobject.png s3://awesomebucket/myobject.png

  To copy object between buckets
  $ obs storage cp s3://awesomebucket/myobject.png s3://destbucket/

  To move object between buckets
  $ obs storage mv s3://awesomebucket/myobject.png s3://destbucket

  To set bucket ACL
  $ obs storage acl s3://awesomebucket private

  To set object ACL
  $ obs storage acl s3://awesomebucket/myobject private

  To show all gmt id policies
  $ obs storage gmt --policy-id

Using Cloudian HyperStore Extension
-----------------------------------

When you run `obs --configure` your will be prompted for your "Cloudian Gmt
Policy" path file. The default value is `notset` which mean you don't want to
use Cloudian extension feature.

To set the path, you can edit "neo.env" file directly or re-run `obs
--configure`. The `neo.env` will look like this:

.. code-block:: bash

    ...
    OBS_USER_URL=mybeloveds3.net
    OBS_USER_GMT_POLICY=/home/john/.config/neo-obs/gmt_policy.yaml
    OBS_ADMIN_USERNAME=john
    ...

Our recommended path is to put it alongside `neo.env` file. The `gmt_policy.yml`
look like this:

.. code-block:: bash

    MYZONE-A:
      id: "od36tj1rvf00wpu33pq5wpu33pq5"
      description: "2 Replication in Foo, 1 in Bar"
      scheme: { "DC2": "2", "DC1": "1"}

    MYZONE-B:
      id: "926cbd3456d36tj1rvf00wpu33pq5"
      description: "1 replica store in zone-1 , 2 replica store in zone-2"
      scheme: {"DC2": "2", "DC1": "1"}
