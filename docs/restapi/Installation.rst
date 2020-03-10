Installation
============

You can run the program via `flask run` or using Docker with specied Dockerfile.

.. code-block:: bash

    #install the requirements
    $ pip3 install -r requirements.txt

    #run program
    $ flask run

Using docker:

.. code-block:: bash

    #build the image
    $docker build -f Dockerfile -t obs-api:0.0.3 .

    #run via docker-compose
    $docker-compose -f obs/api/docker-compose.yml up

Set Environment
---------------

If you use 'flask run' you can insert environment with

.. code-block:: bash
    
    $ export env_name=value

With Docker, you can edit environment value in docker-compose.yml