import requests
import hmac
from hashlib import sha256
from urllib import urlencode
from .payments import Payments
from .banks import Banks
from .receivers import Receivers

API_BASE = 'https://khipu.com/api/2.0'

class Client():
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

    def __make_signature(self, method, params=None, data=None):
        method_name = method.upper()
        hasher = hmac.new(self.secret, digestmod=sha256)
        to_sign = method_name
        if params:
            sorted_items = sorted(params.items(), key = lambda item: item[0])
            to_sign = '&'.join([to_sign, urlencode(sorted_items)])
        if data:
            sorted_items = sorted(data.items(), key = lambda item: item[0])
            to_sign = '&'.join([to_sign, urlencode(sorted_items)])
        hasher.update(to_sign)

        return "{id}:{hash}".format(id=self.receiver_id,
            hash=hasher.hexdigest())

    def make_request(self, method, endpoint, params=None, data=None):
        url = API_BASE + endpoint
        payload = { 'headers': {
            'Authorization': self.__make_signature(method, params, data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'pykhipu/0.1.0',
            'Accept': 'application/json'
        }}

        if params:
            payload.update({ 'params': params })
        if data:
            payload.update({ 'data': data })

        return requests.request(method, url, **payload)
