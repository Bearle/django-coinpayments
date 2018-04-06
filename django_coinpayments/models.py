# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel
import uuid
from django.utils import timezone
from .coinpayments import CoinPayments
from .exceptions import CoinPaymentsProviderError
from .utils import get_coins_list
import datetime
from decimal import Decimal


class CoinPaymentsTransaction(TimeStampedModel):
    id = models.CharField(max_length=100, verbose_name='id', primary_key=True, editable=False)
    address = models.CharField(max_length=150, verbose_name='Address')
    amount = models.DecimalField(max_digits=100, decimal_places=18, verbose_name='Amount')
    confirms_needed = models.PositiveSmallIntegerField(verbose_name='Confirms needed')
    qrcode_url = models.URLField(verbose_name='QR Code Url')
    status_url = models.URLField(verbose_name='Status Url')
    timeout = models.DateTimeField(verbose_name='Valid until')

    def __str__(self):
        return self.id


class PaymentManager(models.Manager):
    def get_late_payments(self):
        """
        Returns payments that are already late by timeout, not filtering their status
        """
        return self.get_queryset().filter(provider_tx__isnull=False,
                                          provider_tx__timeout__lte=timezone.now())

    def get_cancelled_payments(self):
        """
        Returns payments that are already late and should be timed out
        """
        return self.get_late_payments().filter(status__in=[self.model.PAYMENT_STATUS_PENDING])

    def get_timed_out_payments(self):
        """
        Returns payments that are timed out
        """
        return self.get_late_payments().filter(status__in=[self.model.PAYMENT_STATUS_TIMEOUT])

    def mark_timed_out_payments(self):
        """
        Marks late payments as timed out
        """
        return self.get_late_payments().update(status=self.model.PAYMENT_STATUS_TIMEOUT)

    def get_successful_payments(self):
        """
        Returns successfully paid payments
        """
        return self.get_queryset().filter(status__in=[self.model.PAYMENT_STATUS_PAID])


class Payment(TimeStampedModel):
    PAYMENT_STATUS_PAID = 'PAID'
    PAYMENT_STATUS_TIMEOUT = 'TOUT'
    PAYMENT_STATUS_PENDING = 'PEND'
    PAYMENT_STATUS_PROVIDER_PENDING = 'PRPE'
    PAYMENT_STATUS_CANCELLED = 'CNCL'
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PROVIDER_PENDING, 'Provider-related payment pending'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_CANCELLED, 'Cancelled'),
        (PAYMENT_STATUS_TIMEOUT, 'Timed out'),
        (PAYMENT_STATUS_PAID, 'Paid')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency_original = models.CharField(max_length=8, choices=get_coins_list())
    currency_paid = models.CharField(max_length=8, choices=get_coins_list())
    amount = models.DecimalField(max_digits=100, decimal_places=18, verbose_name='Amount')
    amount_paid = models.DecimalField(max_digits=100, decimal_places=18, verbose_name='Amount paid')
    provider_tx = models.OneToOneField(CoinPaymentsTransaction, on_delete=models.CASCADE,
                                       verbose_name='Payment transaction', null=True, blank=True)
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS_CHOICES)
    objects = PaymentManager()

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.amount} of {self.amount_paid} - {self.get_status_display()}'

    def is_paid(self):
        return self.status == self.PAYMENT_STATUS_PAID

    def amount_left(self):
        return self.amount - self.amount_paid

    def is_cancelled(self):
        if self.provider_tx:
            return self.provider_tx.timeout < timezone.now()

    def create_tx(self, invoice=None, **kwargs):
        """
        :param invoice: Field for custom use. Default - payment id
        :param kwargs:
            address      The address to send the funds to in currency_paid network
            buyer_email  Optionally (but highly recommended) set the buyer's email address.
                         This will let us send them a notice if they underpay or need a refund.
            buyer_name   Optionally set the buyer's name for your reference.
            item_name    Item name for your reference,
                         will be on the payment information page and in the IPNs for the transaction.
            item_number  Item number for your reference,
                         will be on the payment information page and in the IPNs for the transaction.
            custom       Field for custom use.
            ipn_url      URL for your IPN callbacks.
                         If not set it will use the IPN URL in your Edit Settings page if you have one set.
        :return: `CoinPaymentsTransaction` instance
        """
        obj = CoinPayments.get_instance()
        if not invoice:
            invoice = self.id
        params = dict(amount=self.amount_left(), currency1=self.currency_original,
                      currency2=self.currency_paid, invoice=invoice)
        params.update(**kwargs)
        result = obj.create_transaction(params)
        if result['error'] == 'ok':
            result = result['result']
            timeout = timezone.now() + datetime.timedelta(seconds=result['timeout'])
            c = CoinPaymentsTransaction.objects.create(id=result['txn_id'], amount=Decimal(result['amount']),
                                                       address=result['address'],
                                                       confirms_needed=int(result['confirms_needed']),
                                                       qrcode_url=result['qrcode_url'], status_url=result['status_url'],
                                                       timeout=timeout)
            self.provider_tx = c
            self.save()
        else:
            raise CoinPaymentsProviderError(result['error'])

        return c
