import requests
import hmac
from hashlib import sha256
from urllib import urlencode

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

    def make_request(self, method, endpoint, params=None, data=None):
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

        url = API_BASE + endpoint

        signature = "{id}:{hash}".format(id=self.receiver_id,
            hash=hasher.hexdigest())

        payload = { 'headers': {
            'Authorization': signature,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'pykhipu/0.1.0',
            'Accept': 'application/json'
        }}

        if params:
            payload.update({ 'params': params })
        if data:
            payload.update({ 'data': data })

        return requests.request(method_name, url, **payload)
