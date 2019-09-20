Admin Usage
=============

.. code-block:: bash

  $ obs admin --help
    Usage: obs admin [OPTIONS] COMMAND [ARGS]...

    administrate object storage.

  Options:
    --help  Show this message and exit.

  Commands:
    cred  administrate user credentials.
    qos   administrate QoS.
    user  administrate user.


Usage Example
-------------

.. code-block:: bash

  To list all available users with certain limit
  $ obs admin user ls --group-id awsmgroup --user-type all --user-status active --limit 2

  To remove a user
  $ obs admin user rm --user-id johndoe --group-id awsmgroup

  To get QoS info
  $ obs admin qos info --user-id johndoe --group-id awsmgroup

  To set QoS limit
  $ obs admin qos set --user-id johndoe --group-id awsmgroup --limit -10

  To show user credentials
  $ obs admin cred ls --user-id StageTest --group-id awsmgroup
