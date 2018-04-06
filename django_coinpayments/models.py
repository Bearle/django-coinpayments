# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel
import uuid
from django.utils import timezone
from .coinpayments import CoinPayments
from .exceptions import CoinPaymentsProviderError
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
    currency_original = models.CharField(max_length=8, choices=CURRENCY_CHOICES)
    currency_paid = models.CharField(max_length=8, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=100, decimal_places=18, verbose_name='Amount')
    amount_paid = models.DecimalField(max_digits=100, decimal_places=18, verbose_name='Amount paid')
    provider_tx = models.OneToOneField(CoinPaymentsTransaction, on_delete=models.CASCADE,
                                       verbose_name='Payment transaction', null=True, blank=True)
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS_CHOICES)

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

    @classmethod
    def get_timed_out_payments(cls):
        return cls.objects.filter(provider_tx__isnull=False, status__in=[cls.PAYMENT_STATUS_PENDING],
                                  provider_tx__timeout__lte=timezone.now())

    def create_tx(self, buyer_email='', buyer_name='', invoice=None, item_name='', item_number=''):
        obj = CoinPayments.get_instance()
        if not invoice:
            invoice = self.id
        params = dict(amount=self.amount_left(), currency1=self.currency_original,
                      currency2=self.currency_paid, buyer_email=buyer_email,
                      buyer_name=buyer_name, item_name=item_name, item_number=item_number,
                      invoice=self.id)
        result = obj.createTransaction(params)
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
