.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="Neo-Obs logo" src="https://raw.githubusercontent.com/BiznetGIO/blobs/master/neo-obs/logo.png" height="150" width="500">
        </a>
    </p>
    <p align="center">
        <!-- <a href="https://pypi.python.org/pypi/neo-obs"><img alt="Pypi version" src="https://img.shields.io/pypi/v/neo-obs.svg"></a> -->
        <!-- <a href="https://pypi.python.org/pypi/neo-obs"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/neo-obs.svg"></a> -->
      <a href="https://neo-obs.readthedocs.io/en/latest/"><img alt="Documentation" src="https://img.shields.io/readthedocs/neo-obs.svg"></a>
      <a href="https://travis-ci.org/BiznetGIO/neo-obs/"><img alt="Build status" src="https://img.shields.io/travis/BiznetGIO/neo-obs.svg"></a>
      <a href="https://github.com/python/black"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
        <!-- <a href="https://pypi.org/project/neo-obs/"><img alt="License" src="https://img.shields.io/pypi/l/neo-cli.svg"></a> -->
    </p>
    <p align="center">
        <a href="#readme">
            <img alt="Neo-Obs demo" src="https://raw.githubusercontent.com/BiznetGIO/blobs/master/neo-obs/demo.gif">
        </a>
    </p>

=========


**neo-obs** is a CLI application which aims to bring the ease of using neo
object storage directly from your terminal.

Did you ever want to use the full power of object storage directly from
terminal?. neo-obs created for the reason. Not only that, but this app can also
manage storage as an admin, such as Cloudian CMC.

.. end-of-readme-intro

Installation
------------


.. code-block:: bash

    $ pip install neo-obs
    $ obs --configure


Features
--------

* Supports for common commands for managing storage: `ls`, `rm`, `get`, `put`,
  `cp`, `mv` `du`, `info`, `sets ACL`, `presign URL` `create bucket`, etc.
* Common commands for admin: `ls users`, `user info`, `rm user`, `set QoS`, etc.
* Can be used as library for your next object storage application.

Take the tour
-------------

Move object into other bucket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ obs storage mv awesomebuck duckduckbuck TODO
    Object "TODO" moved to "awesomebuck" bucket successfully


Get user info
^^^^^^^^^^^^^

.. code-block:: bash

    $ obs admin user info --user-id johndoe --group-id awesome
    ID: johndoe
    Name: John Doe
    Email: johndoe@geemail.com
    Address: 456 Shakedown St
    City: Portsmouth
    Group ID: awesome
    Canonical ID: 5ac765187f93d3f1cef81fake123
    Active: true

Show user's credentials
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ obs admin cred ls --user-id johndoe --group-id awesome
    Access Key: 394b287c9efakekey
    Secret Key: mq7Pn8bonHNfTjfakekey1234
    Created: 2017-11-10 03:19:18+0700 (WIB)
    Active: True

.. end-of-readme-usage

Project information
-------------------

* `Documentation <https://neo-obs.readthedocs.io/en/latest/>`_
* `Contributing <https://biznetgio.github.io/guide/engineering/contrib-guide/>`_
* `Changelog <CHANGELOG.rst>`_
* `License <LICENSE>`_
