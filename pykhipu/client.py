# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import requests
import hmac
import logging
if sys.version_info.major < 3 or sys.version_info.minor < 9:
    from importlib_metadata import version
else:
    from importlib.metadata import version
from hashlib import sha256
from six.moves.urllib.parse import urlencode, quote
#from urllib.parse import urlencode, quote
from pykhipu.payments import Payments
from pykhipu.banks import Banks
from pykhipu.receivers import Receivers

API_BASE = 'https://khipu.com/api/2.0'
TRUE_LIST = [True, 'True', 'true', 'TRUE', 1, '1']
FALSE_LIST = [False, 'False', 'false', 'FALSE', 0, '0']

class Client(object):
    def __init__(self, receiver_id=None, secret=None, debug=False):
        self.receiver_id = receiver_id
        self.secret = secret
        self.is_debug = debug

    @property
    def receiver_id(self):
        return self._receiver_id or os.getenv('KHIPU_RECEIVER_ID')

    @receiver_id.setter
    def receiver_id(self, value):
        self._receiver_id = value

    @property
    def secret(self):
        return self._secret or os.getenv('KHIPU_SECRET')

    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def is_debug(self):
        return self._debug or (os.getenv('KHIPU_DEBUG') in TRUE_LIST)

    @is_debug.setter
    def is_debug(self, value):
        self._debug = (
            value in TRUE_LIST
            and value not in FALSE_LIST
        )
    
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

        hasher = hmac.new(self.secret.encode(), to_sign.encode('UTF-8'), digestmod=sha256)
        signature = "{id}:{hash}".format(id=self.receiver_id,
            hash=hasher.hexdigest())

        if self.is_debug:
            logging.debug('a firmar: %s', to_sign)
            logging.debug('firma: %s', signature)

        return signature

    def make_request(self, method, endpoint, params=None, data=None):
        url = API_BASE + endpoint
        signature = self.__make_signature(method, url, params, data)
        payload = {
            'headers': {
                'Authorization': signature,
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'pykhipu/{version}'.format(version=version('pykhipu')),
                'Accept': 'application/json'
            }
        }

        if params:
            payload.update({ 'params': params })
        if data:
            payload.update({ 'data': data })

        response = requests.request(method, url, **payload)

        if self.is_debug:
            logging.debug('Response: %s', response.text)

        return response
