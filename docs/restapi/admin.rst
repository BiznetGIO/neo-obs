Admin API
=========

.. contents::
   :local:

User
----

List Avaible User
~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    GET api/admin/user

Query Parametes:

===========  =======   =====================
Name         Type      Description          
===========  =======   =====================
groupId      string    name of user group         
user_type    string    type of user         
user_status  string    status of user       
limit        integer   number of user shown 
===========  =======   =====================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: [
        {
        userId: John,
        userType: User,
        fullName: JohnDoe,
        emailAddr: foo@bar.com,
        address1: ,
        address2: null,
        city: Jakarta,
        state: Indonesia,
        zip: 00000,
        country: Indonesia,
        phone: 021-2345,
        groupId: foo,
        website: foo.net,
        active: true,
        canonicalUserId: 123,
        ldapEnabled: false
        },
        {
        userId: Foo,
        userType: User,
        fullName: Foobar,
        emailAddr: foo@bar.com,
        address1: ,
        address2: null,
        city: Jakarta,
        state: Indonesia,
        zip: 00000,
        country: Indonesia,
        phone: 021-230299,
        groupId: foo,
        website: foo.net,
        active: true,
        canonicalUserId: 999,
        ldapEnabled: false
        },
      ]
    status: success,
    message: Operation succeeded
    }

Get User Information
~~~~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    GET api/admin/user

Query Parametes:

===========  =======   ===================
Name         Type      Description        
===========  =======   ===================
groupId      string    name of user group 
userId       string    name of user       
===========  =======   ===================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: {
        userId: John,
        userType: User,
        fullName: JohnDoe,
        emailAddr: foo@bar.com,
        address1: ,
        address2: null,
        city: Jakarta,
        state: Indonesia,
        zip: 00000,
        country: Indonesia,
        phone: 021-2345,
        groupId: foo,
        website: foo.net,
        active: true,
        canonicalUserId: 123,
        ldapEnabled: false
        },
    status: success,
    message: Operation succeeded
    } 

Create New User
~~~~~~~~~~~~~~~
 
.. code-block:: bash

    POST api/admin/user

Query Parametes:

===========  =======   ===================== =================
Name         Type      Description           Status
===========  =======   ===================== =================
groupId      string    name of user group    Required
userId       string    name of user          Required
userType     string    type of user          default ("user")
fullName     string    user full name        Required
emailAddr    string    user email address     
address1     string    user home address      
city         string    user cities           
state        string    user state             
zip          string    user zip code         
country      string    user country          
phone        string    user phone number      
website      string    user website address   
active       boolean   user active status    default (True)
ldapEnabled  boolean   user ldap status      default (False)
===========  =======   ===================== =================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: User John created successfully.
    } 

Suspend User
~~~~~~~~~~~~
 
.. code-block:: bash

    PUT api/admin/user

Query Parametes:

===========  =======   ===================
Name         Type      Description
===========  =======   ===================
groupId      string    name of user group
userId       string    name of user
suspend      boolean   status of suspend
===========  =======   ===================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: null,
    status: success,
    message: User has been suspended.
    }  

Delete User
~~~~~~~~~~~~
 
.. code-block:: bash

    DELETE api/admin/user

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: null,
    status: success,
    message: User John deleted successfully.
    }  

QoS
---

Get Quota User
~~~~~~~~~~~~~~
 
.. code-block:: bash

    GET api/admin/qos

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: {
        groupId: test,
        userId: foo,
        labelId: qos.userQosOverrides.title,
        qosLimitList: [
            {
                type: STORAGE_QUOTA_KBYTES,
                value: -1
            },
            {
                type: REQUEST_RATE_LW,
                value: -1
            },
            {
                type: REQUEST_RATE_LH,
                value: -1
            },
            {
                type: DATAKBYTES_IN_LW,
                value: -1
            },
            {
                type: DATAKBYTES_IN_LH,
                value: -1
            },
            {
                type: DATAKBYTES_OUT_LW,
                value: -1
            },
            {
                type: DATAKBYTES_OUT_LH,
                value: -1
            },
            {
                type: STORAGE_QUOTA_COUNT,
                value: -1
            }
        ],
        Storage Limit: unlimited
    },
    status: success,
    message: Operation succeeded
    }

Set User Quota
~~~~~~~~~~~~~~
 
.. code-block:: bash

    POST api/admin/qos

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
limit        integer   user storage size
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: User John quota changed successfully.
    } 

Delete User Quota
~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    DELETE api/admin/qos

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: null,
    status: success,
    message: User foo quota changed to unlimited.
    }

Credential
----------

Get User Credential
~~~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    GET api/admin/cred

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: [
        {
            accessKey: 123,
            secretKey: 123,
            createDate: 0,
            active: true
        },
        {
            accessKey: 134,
            secretKey: 234,
            createDate: 0,
            active: false
        }
    ],
    status: success,
    message: Operation succeeded
    } 

Create New Credential
~~~~~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    POST api/admin/cred

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 201,
    count: 0,
    data: null,
    status: success,
    message: User foo new credential created successfully.
    } 

Activate/Deactive User Credential
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    PUT api/admin/cred

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key
status       boolean   status of user Credential
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: null,
    status: success,
    message: Credential status has been deactivated.
    }
    
Delete User Credential
~~~~~~~~~~~~~~~~~~~~~~
 
.. code-block:: bash

    DELETE api/admin/cred

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
access_key   string    user access key
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 0,
    data: null,
    status: success,
    message: Access key 123 deleted successfully.
    }

Usage
-----

Get User Usage
~~~~~~~~~~~~~~
 
.. code-block:: bash

    GET api/admin/usage

Query Parametes:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
groupId      string    name of user group
userId       string    name of user
===========  =======   ===========================

Response :

.. code-block:: bash

    {
    code: 200,
    count: 8,
    data: {
        groupId: Foobar,
        userId: John,
        region: stage,
        operation: SB,
        uri: ,
        timestamp: 0,
        value: 400,
        count: 0,
        whitelistValue: 0,
        whitelistCount: 0,
        maxValue: 0,
        whitelistMaxValue: 0,
        ip: ,
        bucket: null,
        policyId: null,
        averageValue: 400,
        whitelistAverageValue: 0
    },
    status: success,
    message: Operation succeeded
    }

