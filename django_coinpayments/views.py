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

# payment = Payment.objects.create(currency_original=tariff.currency, currency_paid=form_data['currency'],
#                                          status=PAYMENT_STATUS_PROVIDER_PENDING,
#                                          amount=tariff.cost, amount_paid=decimal.Decimal(0), order=order)
# return create_tx_and_redirect(payment, form_data['name'], service.pk)

# def create_tx_and_redirect(payment, name, number):
#     try:
#         tx = payment.create_tx(item_name=name, item_number=number)
#         payment.status = PAYMENT_STATUS_PENDING
#         payment.save()
#         return redirect(reverse('main:payment_detail', kwargs={'pk': payment.pk}))
#     except ProviderError as e:
#         # TODO redirect to error page with info about provider error
#         return ''
#
# def create_new_payment(request, pk):
#     payment = get_object_or_404(Payment, pk)
#     if payment.status in [PAYMENT_STATUS_PROVIDER_PENDING, PAYMENT_STATUS_TIMEOUT]:
#         pass
#     elif payment.status in [PAYMENT_STATUS_PENDING]:
#         payment.provider_tx.delete()
#     else:
#         # TODO: redirect to payment status mismatch error page
#         return ''
#     service = payment.order.get_service()
#     return create_tx_and_redirect(payment, service.name, service.pk)
