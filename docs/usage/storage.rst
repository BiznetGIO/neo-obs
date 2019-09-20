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
  info     Display bucket or object info.
  ls       List bucket or object.
  mb       Create bucket.
  mkdir    Create directory inside bucket
  mv       Move object into other bucket.
  presign  Generate Url for bucket or object.
  put      Upload object to bucket.
  rm       Remove bucket or object.


Every time you want to know avaliable arguments and options for certain command,
don't hesitate to run `--help`

.. code-block:: bash

  $ obs storage mv --help
  Usage: obs storage mv [OPTIONS] [SRC_BUCKET] [DEST_BUCKET] [OBJECT_NAME]

    Move object into other bucket.

  Options:
    --help  Show this message and exit.

See, I get the help message above which mean, I need to run the command below to
move object

.. code-block:: bash

  $ obs storage mv sourcebucket destinationbucket awesomeobject



Usage Example
-------------

.. code-block:: bash

  To list all available buckets
  $ obs storage ls

  To list all object inside spesific buckets
  $ obs storage ls awesomebucket

  To list all object inside spesific "directory"
  $ obs storage ls awesomebucket -p foo-dir

  To remove a bucket
  $ obs storage rm awesomebucket

  To remove object inside bucket
  $ obs storage rm awesomebucket myobject

  To make a bucket
  $ obs storage mb awesomebucket

  To make a bucket suffixed with random string
  $ obs storage mb awesomebucket --random

  To make a bucket with spesific ACL
  $ obs storage mb awesomebucket --acl private

  To download an object
  $ obs storage get awesomebucket myobject

  To upload an object with specified name
  [bucket name] [path] [object name]
  $ obs storage put awesomebucket /path/to/myobject myawesomeobject

  To upload an object with base name instead
  $ obs storage put awesomebucket /path/to/myobject --use-basename

  To copy object between buckets
  $ obs storage cp awesomebucket destbucket myobject

  To move object between buckets
  $ obs storage mv awesomebucket destbucket myobject

  To set bucket ACL
  $ obs storage acl awesomebucket private

  To set object ACL
  $ obs storage acl awesomebucket myobject private
