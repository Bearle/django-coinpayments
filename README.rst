=============================
django-coinpayments
=============================

.. image:: https://badge.fury.io/py/django-coinpayments.svg
    :target: https://badge.fury.io/py/django-coinpayments

.. image:: https://travis-ci.org/delneg/django-coinpayments.svg?branch=master
    :target: https://travis-ci.org/delneg/django-coinpayments

.. image:: https://codecov.io/gh/delneg/django-coinpayments/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/delneg/django-coinpayments

Package for payment handling via https://www.coinpayments.net

Documentation
-------------

The full documentation is at https://django-coinpayments.readthedocs.io.

Quickstart
----------

Install django-coinpayments::

    pip install django-coinpayments

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_coinpayments.apps.DjangoCoinpaymentsConfig',
        ...
    )


**Important!**

You have to provide API keys with `create_transaction`, `get_tx_info`, `rates` permissions like this in your settings.py:

.. code-block:: python

    COINPAYMENTS_API_KEY = 'aaaaa'
    COINPAYMENTS_API_SECRET = 'aaa'

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
