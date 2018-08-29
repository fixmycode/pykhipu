# -*- coding: utf-8 -*-
import requests
import hmac
from hashlib import sha256
from urllib import urlencode, quote
from .payments import Payments
from .banks import Banks
from .receivers import Receivers

API_BASE = 'https://khipu.com/api/2.0'

class Client(object):
    def __init__(self, receiver_id=None, secret=None, debug=False):
        self._receiver_id = receiver_id
        self._secret = secret
        self._debug = debug

    @property
    def receiver_id(self):
        return self._receiver_id

    @property
    def secret(self):
        return self._secret

    @property
    def is_debug(self):
        return self._debug

    @property
    def payments(self):
        if not hasattr(self, '_payments'):
            self._payments = Payments(self)
        return self._payments

    @property
    def banks(self):
        if not hasattr(self, '_banks'):
            self._banks = Banks(self)
        return self._banks

    @property
    def receivers(self):
        if not hasattr(self, '_receivers'):
            self._receivers = Receivers(self)
        return self._receivers

    def __make_signature(self, method, url, params=None, data=None):
        method_name = method.upper()
        to_sign = '&'.join([method_name, quote(url, safe='')])

        def quote_items(tuples):
            return ['='.join([quote(str(pair[0]), safe=''),
                quote(str(pair[1]), safe='')]) for pair in tuples]

        if params:
            sorted_items = sorted(params.items(), key = lambda item: item[0])
            to_sign = '&'.join([to_sign,] + quote_items(sorted_items))
        if data:
            sorted_items = sorted(data.items(), key = lambda item: item[0])
            to_sign = '&'.join([to_sign,] + quote_items(sorted_items))

        hasher = hmac.new(self.secret, to_sign, digestmod=sha256)
        signature = "{id}:{hash}".format(id=self.receiver_id,
            hash=hasher.hexdigest())

        if self.is_debug:
            print(u"A firmar: {0}".format(to_sign))
            print(u"Firma: {0}".format(signature))

        return signature

    def make_request(self, method, endpoint, params=None, data=None):
        url = API_BASE + endpoint
        signature = self.__make_signature(method, url, params, data)
        payload = {
            'headers': {
                'Authorization': signature,
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'pykhipu/0.1.3',
                'Accept': 'application/json'
            }
        }

        if params:
            payload.update({ 'params': params })
        if data:
            payload.update({ 'data': data })

        response = requests.request(method, url, **payload)

        if self.is_debug:
            print(u"Response: {0}".format(response.text))

        return response
