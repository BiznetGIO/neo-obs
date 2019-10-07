Tips
====

Bash Completion
---------------

To activate bash completions for obs-cli. Run:

.. code-block:: bash

  $ eval "$(_OBS_COMPLETE=source obs)"

Or add that command to your bash profile to set it permanently.

Bash Alias
----------

To make your command shorter. Rather than typing `obs storage` or `obs admin`
you can use `obss` and `obsa` by adding these line to your bash profile:

.. code-block:: bash

    alias obss="obs storage"
    alias obsa="obs admin"
