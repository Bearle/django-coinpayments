=====
Usage
=====

To use django-coinpayments in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_coinpayments.apps.DjangoCoinpaymentsConfig',
        ...
    )

Add django-coinpayments's URL patterns:

.. code-block:: python

    from django_coinpayments import urls as django_coinpayments_urls


    urlpatterns = [
        ...
        url(r'^', include(django_coinpayments_urls)),
        ...
    ]
