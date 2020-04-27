Storage API
===========

.. contents::
   :local:

Get List Buckets
----------------
 
.. code-block:: bash

    GET api/storage/list

Query Parameters:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key 
secret_key   string    user secret key
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: [
        {
            name: luck,
            creation_date: 2020-03-02 06:38:53
        },
        {
            name: ranger,
            creation_date: 2020-03-02 06:51:12
        }
    ],
    ...
    } 

Get List Objects
----------------
 
.. code-block:: bash

    GET api/storage/list

Query Parameters:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key 
secret_key   string    user secret key
bucket_name  string    name of bucket
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 2,
    data: [
        {
            directory: Folder/
        },
        {
            Key: tes.png,
            LastModified: 2020-02-02 00:00:00,
            ETag: 000tes,
            Size: 0,
            StorageClass: STANDARD,
            Owner: {
                DisplayName: JohnDoe,
                ID: 123
            }
        }
    ],
    status: success,
    message: Operation succeeded
    } 

Get Bucket Info
---------------
 
.. code-block:: bash

    GET api/storage/bucket/:bucket_name

Query Parameters:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key 
secret_key   string    user secret key
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: {
        ACL: [
            [
                JohnDoe,
                FULL_CONTROL
            ]
        ],
        CORS: null,
        Policy: null,
        Expiration: null,
        Location: null,
        GmtPolicy: Replica Data to all nodes within single Datacenter
    },
    status: success,
    message: Operation succeeded
    }

Create New Bucket
-----------------
 
.. code-block:: bash

    POST api/storage/bucket/:bucket_name

Query Parameters:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key 
secret_key   string    user secret key
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: Bucket bucket1 created successfully.
    }

Delete Bucket
-------------
 
.. code-block:: bash

    DELETE api/storage/bucket/:bucket_name

Query Parameters:

===========  =======   =========================== 
Name         Type      Description 
===========  =======   =========================== 
access_key   string    user access key 
secret_key   string    user secret key 
===========  =======   =========================== 

Response :

.. code-block:: bash

    {
    code: 200,
    count: 1,
    data: {
        ResponseMetadata: {
            RequestId: a-b-123,
            HostId: ,
            HTTPStatusCode: 204,
            HTTPHeaders: {
                date: Mon, 02 Feb 2020 00:00:00 GMT,
                x-amz-request-id: a-b-123,
                server: CloudianS3
            },
            RetryAttempts: 0
        }
    },
    status: success,
    message: Bucket ranger deleted successfully.
    } 

Get Object Info
---------------
 
.. code-block:: bash

    GET api/storage/object/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object with extension
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 6,
    data: {
        ACL: [['JohnDoe', 'FULL_CONTROL']],
        Size: 30811,
        LastModified: 2020-02-02 00:00:00+00:00,
        MD5: \e123\,
        MimeType: binary/octet-stream,
        StorageClass: None
    },
    status: success,
    message: Operation succeeded
    } 

Delete Object
-------------
 
.. code-block:: bash

    DELETE api/storage/object/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object with extension
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 1,
    data: {
        ResponseMetadata: {
            RequestId: a-b-123,
            HostId: ,
            HTTPStatusCode: 204,
            HTTPHeaders: {
                date: Mon, 02 Feb 2020 00:00:00 GMT,
                x-amz-request-id: a-b-123,
                server: CloudianS3
            },
            RetryAttempts: 0
        }
    },
    status: success,
    message: Object Foo.png deleted successfully.
    }

Upload Object
-------------
 
.. code-block:: bash

    POST api/storage/object/upload/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object with extension
files        form      object files
acl          string    acl access for object
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: Object foo.png uploaded successfully.
    }

Download Object
---------------
 
.. code-block:: bash

    GET api/storage/object/download/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object or directory with extension
===========  =======   =============================

.. Note:: 
    Use object_name with path to download objec, directory path to download directory, and don't use paramater key to download all object in bucket.

Example:

    * object.png

    * folder/directory/first/

Response :

.. code-block:: bash

    API returned/downloaded object

Move Object
-------------
 
.. code-block:: bash

    POST api/storage/object/move/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object with extension
move_to      string    name of destination bucket
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: Object foo.png moved successfully.
    }

Copy Object
-------------
 
.. code-block:: bash

    POST api/storage/object/copy/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
object_name  string    name of object with extension
copy_to      string    name of destination bucket
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: Object foo.png copied successfully.
    }

Get Usage
---------
 
.. code-block:: bash

    GET api/storage/usage

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
bucket_name  string    name of bucket
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 2,
    data: {
        bucket: [
            {
                name: bucket1,
                size: 30811,
                objects: 1
            }
        ],
        total_usage: 30811
    },
    status: success,
    message: Operation succeeded
    }

Create New Directory
--------------------
 
.. code-block:: bash

    POST api/storage/mkdir/:bucket_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
directory    string    name of directory
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 2,
    data: {
        ResponseMetadata: {
            RequestId: a-b-123,
            HostId: ,
            HTTPStatusCode: 200,
            HTTPHeaders: {
                date: Mon, 02 Feb 2020 00:00:00 GMT,
                x-amz-request-id: a-b-123,
                etag: \e123\,
                content-length: 0,
                server: CloudianS3
            },
            RetryAttempts: 0
        },
        ETag: \e123\
    },
    status: success,
    message: Directory Folder added successfully.
    }

Get URL Object
--------------
 
.. code-block:: bash

    GET api/storage/presign/:bucket_name/:object_name

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
expire       integer   URL expired time in seconds
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 141,
    data: http;//url-test.net,
    status: success,
    message: Operation succeeded
    }

Set ACL
--------------
 
.. code-block:: bash

    GET api/storage/acl

Query Parameters:

===========  =======   =============================
Name         Type      Description
===========  =======   =============================
access_key   string    user access key 
secret_key   string    user secret key
bucket_name  string    name of bucket
object_name  string    name of object with extension
===========  =======   =============================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 1,
    data: {
        ResponseMetadata: {
            ResponseMetadata: {
            RequestId: a-b-123,
            HostId: ,
            HTTPStatusCode: 200,
            HTTPHeaders: {
                date: Mon, 02 Feb 2020 00:00:00 GMT,
                x-amz-request-id: a-b-123,
                etag: \e123\,
                content-length: 0,
                server: CloudianS3
            },
            RetryAttempts: 0
        },
    },
    status: success,
    message: Added public-read access to object foo.png.
    } 

Get GMT Policy
--------------
 
.. code-block:: bash

    GET api/storage/gmt

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: [
        {
            Name: gmt-1,
            Id: 123,
            Description: No description
        },
        {
            Name: gmt-2,
            Id: 345,
            Description: No description
        },
    ],
    status: success,
    message: Operation succeeded
    }

