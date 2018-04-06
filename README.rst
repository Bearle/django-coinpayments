=============================
django-coinpayments
=============================

.. image:: https://badge.fury.io/py/django-coinpayments.svg
    :target: https://badge.fury.io/py/django-coinpayments

.. image:: https://travis-ci.org/Bearle/django-coinpayments.svg?branch=master
    :target: https://travis-ci.org/Bearle/django-coinpayments

.. image:: https://codecov.io/gh/Bearle/django-coinpayments/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Bearle/django-coinpayments

Package for payment handling via https://www.coinpayments.net

Screenshots
-----------

.. image:: https://github.com/Bearle/django-coinpayments/blob/master/screenshots/transaction.jpg?raw=true

Features
--------

* Has full Coinpayments API client based on .. _`This one`: https://github.com/DogFive/pyCoinPayments
* Has celery, cron tasks for transaction status updates
* Provides a simple `create_tx` method
* Multiple accepted coins can be set using COINPAYMENTS_ACCEPTED_COINS variable in settings.py

Dependencies
============

* `django >= 1.9 <http://djangoproject.com/>`_
* `django-model-utils >=2.0 <https://github.com/jazzband/django-model-utils>`_

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
        'django_coinpayments',
        ...
    )

Run ``migrate``::

    python manage.py migrate django_coinpayments


**Important!**

You have to provide API keys with `create_transaction`, `get_tx_info` permissions like this in your settings.py:

.. code-block:: python

    COINPAYMENTS_API_KEY = 'aaaaa'
    COINPAYMENTS_API_SECRET = 'aaa'


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
