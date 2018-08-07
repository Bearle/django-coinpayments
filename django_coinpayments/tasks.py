from celery.utils.log import get_task_logger
from celery import shared_task
from .models import Payment, CoinPaymentsTransaction
from .coinpayments import CoinPayments
from .exceptions import TxInfoException
from django.core.paginator import Paginator
from decimal import Decimal

logger = get_task_logger(__name__)


@shared_task
def refresh_tx_info():
    caller = CoinPayments.get_instance()
    objects = Payment.objects.get_pending_payments().order_by('id')
    # 25 because of https://www.coinpayments.net/apidoc-get-tx-info
    paginator = Paginator(objects, 25)
    for page in paginator.page_range:
        chunk = paginator.page(page).object_list
        provider_txs_ids = [i.provider_tx.id for i in chunk]
        res = caller.get_tx_info_multi({'txid': '|'.join(provider_txs_ids)})
        if res['error'] == 'ok':
            results = res['result']
            for k, v in results.items():
                temp = CoinPaymentsTransaction.objects.filter(id=k).first()
                if not temp:
                    logger.error(
                        'CoinPaymentsTransaction with id %s received from API but not found in DB'.format(str(k)))
                else:
                    payment = temp.payment
                    # Payments statuses: https://www.coinpayments.net/merchant-tools-ipn
                    # Safe statuses: 2 and >= 100
                    if v['status'] == 2 or v['status'] >= 100:
                        logger.info('Received payment for transaction {} - payment {} ({})'
                                    .format(str(k), str(payment.id), str(payment.amount)))
                        payment.amount_paid = payment.amount
                    else:
                        payment.amount_paid = Decimal(v['receivedf'])
                    if payment.amount_paid == payment.amount:
                        payment.status = Payment.PAYMENT_STATUS_PAID
                    payment.save()

        else:
            raise TxInfoException(res['error'])


@shared_task
def set_timeout_for_payments():
    objects = Payment.objects.mark_timed_out_payments()
    return [i.id for i in objects]
