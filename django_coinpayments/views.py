# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	CoinPaymentsTransaction,
	Payment,
)


class CoinPaymentsTransactionCreateView(CreateView):

    model = CoinPaymentsTransaction


class CoinPaymentsTransactionDeleteView(DeleteView):

    model = CoinPaymentsTransaction


class CoinPaymentsTransactionDetailView(DetailView):

    model = CoinPaymentsTransaction


class CoinPaymentsTransactionUpdateView(UpdateView):

    model = CoinPaymentsTransaction


class CoinPaymentsTransactionListView(ListView):

    model = CoinPaymentsTransaction


class PaymentCreateView(CreateView):

    model = Payment


class PaymentDeleteView(DeleteView):

    model = Payment


class PaymentDetailView(DetailView):

    model = Payment


class PaymentUpdateView(UpdateView):

    model = Payment


class PaymentListView(ListView):

    model = Payment

