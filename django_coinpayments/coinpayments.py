import urllib.request, urllib.parse, urllib.error
import hmac
import hashlib
import json
from django.conf import settings, ImproperlyConfigured

class CoinPayments():

    def __init__(self, publicKey, privateKey, ipn_url=None):
        self.url = 'https://www.coinpayments.net/api.php'
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.ipn_url = ipn_url
        self.format = 'json'
        self.version = 1

    @classmethod
    def get_instance(cls):
        if not getattr(settings, 'COINPAYMENTS_API_KEY') or not getattr(settings, 'COINPAYMENTS_API_SECRET'):
            raise ImproperlyConfigured('COINPAYMENTS_API_KEY and COINPAYMENTS_API_SECRET are required!')
        return CoinPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET)

    def createHmac(self, **params):
        """ Generate an HMAC based upon the url arguments/parameters

            We generate the encoded url here and return it to Request because
            the hmac on both sides depends upon the order of the parameters, any
            change in the order and the hmacs wouldn't match
        """
        encoded = bytes(urllib.parse.urlencode(params).encode('ascii'))
        private_key_b = bytes(self.privateKey.encode('ascii'))
        return encoded, hmac.new(private_key_b, encoded, hashlib.sha512).hexdigest()

    def Request(self, request_method, **params):
        """The basic request that all API calls use
            the parameters are joined in the actual api methods so the parameter
            strings can be passed and merged inside those methods instead of the
            request method
        """
        encoded, sig = self.createHmac(**params)

        headers = {'hmac': sig}

        if request_method == 'get':
            req = urllib.request.Request(self.url, headers=headers)
        elif request_method == 'post':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            req = urllib.request.Request(self.url, data=encoded, headers=headers)
        try:
            response = urllib.request.urlopen(req)
            status_code = response.getcode()
            response_body = response.read()
        except urllib.error.HTTPError as e:
            status_code = e.getcode()
            response_body = e.read()
        return json.loads(response_body)

    def createTransaction(self, params=None):
        """ Creates a transaction to give to the purchaser
            https://www.coinpayments.net/apidoc-create-transaction
        """
        if params is None:
            params = {}
        if self.ipn_url:
            params.update({'ipn_url': self.ipn_url})
        params.update({'cmd': 'create_transaction',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getBasicInfo(self, params=None):
        """Gets merchant info based on API key (callee)
           https://www.coinpayments.net/apidoc-get-basic-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_basic_info',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def rates(self, params=None):
        """Gets current rates for currencies
           https://www.coinpayments.net/apidoc-rates
        """
        if params is None:
            params = {}
        params.update({'cmd': 'rates',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def balances(self, params=None):
        """Get current wallet balances
            https://www.coinpayments.net/apidoc-balances
        """
        if params is None:
            params = {}
        params.update({'cmd': 'balances',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getDepositAddress(self, params=None):
        """Get address for personal deposit use
           https://www.coinpayments.net/apidoc-get-deposit-address
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_deposit_address',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getCallbackAddress(self, params=None):
        """Get a callback address to recieve info about address status
           https://www.coinpayments.net/apidoc-get-callback-address
        """
        if params is None:
            params = {}
        if self.ipn_url:
            params.update({'ipn_url': self.ipn_url})
        params.update({'cmd': 'get_callback_address',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def createTransfer(self, params=None):
        """Not really sure why this function exists to be honest, it transfers
            coins from your addresses to another account on coinpayments using
            merchant ID
           https://www.coinpayments.net/apidoc-create-transfer
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_transfer',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def createWithdrawal(self, params=None):
        """Withdraw or masswithdraw(NOT RECOMMENDED) coins to a specified address,
        optionally set a IPN when complete.
            https://www.coinpayments.net/apidoc-create-withdrawal
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_withdrawal',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def convertCoins(self, params=None):
        """Convert your balances from one currency to another
            https://www.coinpayments.net/apidoc-convert
        """
        if params is None:
            params = {}
        params.update({'cmd': 'convert',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getWithdrawalHistory(self, params=None):
        """Get list of recent withdrawals (1-100max)
            https://www.coinpayments.net/apidoc-get-withdrawal-history
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_history',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getWithdrawalInfo(self, params=None):
        """Get information about a specific withdrawal based on withdrawal ID
            https://www.coinpayments.net/apidoc-get-withdrawal-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_info',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getConversionInfo(self, params=None):
        """Get information about a specific withdrawal based on withdrawal ID
            https://www.coinpayments.net/apidoc-get-conversion-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_conversion_info',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)

    def getTxInfoMulti(self, params=None):
        """ Get tx info (up to 25 ids separated by | )
            https://www.coinpayments.net/apidoc-get-tx-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_tx_info_multi',
                       'key': self.publicKey,
                       'version': self.version,
                       'format': self.format})
        return self.Request('post', **params)
