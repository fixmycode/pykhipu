import os
import sys
from unittest import TestCase
if sys.version_info.major < 3:
    from mock import patch
else:
    from unittest.mock import patch
from pykhipu.client import Client


class TestClient(TestCase):
    def test_empty_constructor(self):
        client = Client()
        self.assertIsNone(client.receiver_id)
        self.assertIsNone(client.secret)
        self.assertFalse(client.is_debug)
    
    def test_late_config(self):
        client = Client()
        
        receiver_id = 'A'
        secret = 'B'
        debug = 'C'

        client.receiver_id = receiver_id
        client.secret = secret
        client.is_debug = debug

        self.assertEqual(client.receiver_id, receiver_id)
        self.assertEqual(client.secret, secret)
        self.assertFalse(client.is_debug)

        for value in [True, 'True', 'true', 'TRUE', 1, '1']:
            client.is_debug = value
            self.assertTrue(client.is_debug)

        for value in [False, 'False', 'false', 'FALSE', 0, '0']:
            client.is_debug = value
            self.assertFalse(client.is_debug)
    
    def test_make_signature(self):
        client = Client(receiver_id='A', secret='B')
        method = 'GET'
        url = '/test'
        params = {'test': 'true', 'another': 'ok'}
        data = {'payload': '123'}

        self.assertEqual(client._Client__make_signature(method, url),
            'A:bad6f7d155cafe89c1c69476cfc7d88891b0ed57180c2b3d004010f71f65e1eb')
        self.assertEqual(client._Client__make_signature(method, url, params),
            'A:dd561da205892eb154fd390220ca111b59412be522bdb107f95795e70f9c322d')
        self.assertEqual(client._Client__make_signature(method, url, params, data),
            'A:5735c89d22596d6a3c4d6d904c4d1641533c39912eafca9b080804ee322441fa')

        client.receiver_id = 'C'
        self.assertEqual(client._Client__make_signature(method, url),
            'C:bad6f7d155cafe89c1c69476cfc7d88891b0ed57180c2b3d004010f71f65e1eb')

    def test_make_request(self):
        with patch('pykhipu.client.requests.request') as mock_request:
            mock_request.return_value.ok = True
            client = Client(receiver_id='A', secret='B')
            response = client.make_request('GET', '/test', {'test': 'true'}, {'payload': '1234'})
            self.assertTrue(response.ok)

