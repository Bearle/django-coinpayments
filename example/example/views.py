from django import forms
from django_coinpayments.models import Payment
from django_coinpayments.exceptions import CoinPaymentsProviderError
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import render, get_object_or_404
from decimal import Decimal


class ExamplePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'currency_original', 'currency_paid']


def create_tx(request, payment):
    context = {}
    try:
        tx = payment.create_tx()
        payment.status = Payment.PAYMENT_STATUS_PENDING
        payment.save()
        context['object'] = payment
    except CoinPaymentsProviderError as e:
        context['error'] = e
    return render(request, 'django_coinpayments/payment_result.html', context)


class PaymentDetail(DetailView):
    model = Payment
    template_name = 'django_coinpayments/payment_result.html'
    context_object_name = 'object'


class PaymentSetupView(FormView):
    template_name = 'django_coinpayments/payment_setup.html'
    form_class = ExamplePaymentForm

    def form_valid(self, form):
        cl = form.cleaned_data
        payment = Payment(currency_original=cl['currency_original'],
                          currency_paid=cl['currency_paid'],
                          amount=cl['amount'],
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
        return create_tx(self.request, payment)


class PaymentList(ListView):
    model = Payment
    template_name = 'django_coinpayments/payment_list.html'


def create_new_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if payment.status in [Payment.PAYMENT_STATUS_PROVIDER_PENDING, Payment.PAYMENT_STATUS_TIMEOUT]:
        pass
    elif payment.status in [Payment.PAYMENT_STATUS_PENDING]:
        payment.provider_tx.delete()
    else:
        error = "Invalid status - {}".format(payment.get_status_display())
        return render(request, 'django_coinpayments/payment_result.html', {'error': error})
    return create_tx(request, payment)
