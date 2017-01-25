PyKhipu
=======

Wrapper for the Khipu payment service API v2.0

Installation
------------

::

    pip install pykhipu

Usage
-----

::

    from pykhipu.client import Client
    client = Client(receiver_id='1234', secret='abcd')
    payment = client.payments.post('test', 'USD', 100)
    print(payment.payment_url)
