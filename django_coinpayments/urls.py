# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^CoinPaymentsTransaction/~create/$",
        view=views.CoinPaymentsTransactionCreateView.as_view(),
        name='CoinPaymentsTransaction_create',
    ),
    url(
        regex="^CoinPaymentsTransaction/(?P<pk>\d+)/~delete/$",
        view=views.CoinPaymentsTransactionDeleteView.as_view(),
        name='CoinPaymentsTransaction_delete',
    ),
    url(
        regex="^CoinPaymentsTransaction/(?P<pk>\d+)/$",
        view=views.CoinPaymentsTransactionDetailView.as_view(),
        name='CoinPaymentsTransaction_detail',
    ),
    url(
        regex="^CoinPaymentsTransaction/(?P<pk>\d+)/~update/$",
        view=views.CoinPaymentsTransactionUpdateView.as_view(),
        name='CoinPaymentsTransaction_update',
    ),
    url(
        regex="^CoinPaymentsTransaction/$",
        view=views.CoinPaymentsTransactionListView.as_view(),
        name='CoinPaymentsTransaction_list',
    ),
	url(
        regex="^Payment/~create/$",
        view=views.PaymentCreateView.as_view(),
        name='Payment_create',
    ),
    url(
        regex="^Payment/(?P<pk>\d+)/~delete/$",
        view=views.PaymentDeleteView.as_view(),
        name='Payment_delete',
    ),
    url(
        regex="^Payment/(?P<pk>\d+)/$",
        view=views.PaymentDetailView.as_view(),
        name='Payment_detail',
    ),
    url(
        regex="^Payment/(?P<pk>\d+)/~update/$",
        view=views.PaymentUpdateView.as_view(),
        name='Payment_update',
    ),
    url(
        regex="^Payment/$",
        view=views.PaymentListView.as_view(),
        name='Payment_list',
    ),
	]
