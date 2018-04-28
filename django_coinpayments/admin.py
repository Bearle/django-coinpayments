from django.conf import settings
from django.contrib import admin
from django.urls import reverse, exceptions
from django.utils.html import format_html
from .models import Payment, CoinPaymentsTransaction
from django.utils.translation import ugettext_lazy as _


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency_original', 'currency_paid', 'amount', 'status')
    list_filter = ('status',)


class CoinPaymentsTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'amount', 'link_to_payment')

    def link_to_payment(self, obj):
        if hasattr(obj, 'payment'):
            link = reverse("admin:django_coinpayments_payment_change", args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', link, obj.payment.id)
        return '-'

    link_to_payment.short_description = _('Payment')


if getattr(settings, 'COINPAYMENTS_ADMIN_ENABLED', True):
    admin.site.register(Payment, PaymentAdmin)
    admin.site.register(CoinPaymentsTransaction, CoinPaymentsTransactionAdmin)
