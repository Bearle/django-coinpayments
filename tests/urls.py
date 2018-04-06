# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_coinpayments.urls import urlpatterns as django_coinpayments_urls

urlpatterns = [
    url(r'^', include(django_coinpayments_urls, namespace='django_coinpayments')),
]
