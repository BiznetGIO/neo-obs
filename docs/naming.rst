Naming Guidelines
=================

Bucket Name Rules
-----------------

The following are the rules for naming S3 buckets in neo-OBS:

* Bucket names must be unique.

* Bucket names must comply with DNS naming conventions.

* Bucket names must be at least 3 and no more than 63 characters long.

* Bucket names must not contain uppercase characters or underscores.

* Bucket names must start and end with a lowercase letter or number.

* Bucket names can contain lowercase letters, numbers, and hyphens.

* Bucket names must not be formatted as an IP address (for example, 192.168.5.4).

Example
~~~~~~~

* comp.bucket
* bucket-first
* comp.bucket-second

For more information, see `Bucket Naming Rules <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules>`_

Object Name Rules
-----------------

Any UTF-8 character can be used in an object key name. However, using certain characters in key names can cause problems with some applications and protocols.

Safe Characters
~~~~~~~~~~~~~~~

The following character sets are generally safe for use in key names:

* All of alphanumeric characters

* Exlamation Mark **!**

* Hyphen **-**

* Underscore **_**

* Dot **.**

* Asterisk **\***

* Singel Quote **'**

* Parenthesis **( )**

Characters to Avoid
~~~~~~~~~~~~~~~~~~~

The following characters will be filtered in object name because of significant special handling for consistency across all applications:

* Backslash **\\**

* curly brace **{ }**

* Non-printable ASCII characters (128–255 decimal characters)

* Caret **^**

* Percent character **%**

* Grave accent / back tick **\`**

* square bracket **[ ]**

* Quotation marks **"**

* 'Greater Than' symbol **>**

* Tilde **~**

* 'Less Than' symbol **<**

* 'Pound' character **#**

* Vertical bar / pipe **|**

.. Note:: Characters that not shown in this section might require special handling, either use URL encoding or referenced as HEX


Example
~~~~~~~

* 4my-organization

* my.great_photos-2014/jan/myvacation.jpg

* videos/2014/birthday/video1.wmv


For more information, see `Object Key Naming Guidelines <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#object-key-guidelines>`_

Creating User Rules
-------------------

The following are the rules for creating user in neo-OBS:

* Parameter required to fill when creating user is **user id**, **group id**, **fullname**

* Parameter **user id**  have same rules with bucket naming, see `Bucket Name Rules`_

* The following characters will be filtered when creating user:
    
    * 'Greater Than' symbol **>**

    * 'Less Than' symbol **<**

    * Ampersand **&**

    * Semicolon **;**

    * Vertical bar / pipe **|**

    * Grave accent / back tick **\`**

Example
~~~~~~~

.. code-block:: bash

    active: true,
    address1: Jl. Sudirman,
    address2: ,
    city: Jakarta,
    country: Indonesia,
    emailAddr: JohnT@biznetgio.com,
    fullName: John Thompson,
    groupId: QA,
    ldapEnabled: false,
    phone: (022)23456,
    state: ID,
    userId: John,
    userType: User,
    website: another.web.id,
    zip: 12345

