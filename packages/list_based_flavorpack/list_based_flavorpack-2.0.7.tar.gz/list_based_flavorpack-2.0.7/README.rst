List-Based FlavorPack
=====================

.. image:: https://gitlab.com/serial-lab/list_based_flavorpack/badges/master/pipeline.svg
        :target: https://gitlab.com/serial-lab/list_based_flavorpack/commits/master

.. image:: https://gitlab.com/serial-lab/list_based_flavorpack/badges/master/coverage.svg
        :target: https://gitlab.com/serial-lab/list_based_flavorpack/pipelines




Quickstart
----------

Install the List-Based FlavorPack
---------------------------------

.. code-block:: text

    pip install list_based_flavorpack


Add it to your `INSTALLED_APPS`:

.. code-block:: text

    INSTALLED_APPS = (
        ...
	'serialbox',
        'list_based_flavorpack.apps.ListBasedFlavorpackConfig',
        ...
    )


Run the migrations in your QU4RTET directory:

.. code-block:: text

     python manage.py migrate list_based_flavorpack

Using the List-based Flavorpack
-------------------------------

Installing the List-based Flavorpack will enable new endpoints for serialbox under /serialbox/list-based-regions/

This special type of regions ties together a QU4RTET Capture Rule, QU4RTET OUTPUT endpoints and authentication Info, as well as a QU4RTET Template instance to render special XML.


Running The Unit Tests
----------------------

.. code-block:: text

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

