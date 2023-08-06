=============================
dj-input-flow
=============================

.. image:: https://badge.fury.io/py/dj-input-flow.svg
    :target: https://badge.fury.io/py/dj-input-flow

.. image:: https://travis-ci.org/kverdecia/dj-input-flow.svg?branch=master
    :target: https://travis-ci.org/kverdecia/dj-input-flow

.. image:: https://codecov.io/gh/kverdecia/dj-input-flow/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kverdecia/dj-input-flow

Django app to handle data flow

Documentation
-------------

The full documentation is at https://dj-input-flow.readthedocs.io.

Quickstart
----------

Install dj-input-flow::

    pip install dj-input-flow

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'adminsortable',
        'inputflow',
        ...
    )

Add dj-input-flow's URL patterns:

.. code-block:: python

    from inputflow import urls as inputflow_urls


    urlpatterns = [
        ...
        url(r'^inputflow/', include(inputflow_urls)),

        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
