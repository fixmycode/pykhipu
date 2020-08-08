# PyKhipu

Paquete de Python para el API 2.0 del servicio de pagos Khipu

🇬🇧 Python wrapper for the Khipu payment service API v2.0

![PyPI](https://img.shields.io/pypi/v/pykhipu)

## Sobre Khipu

> [Khipu](https://cl.khipu.com/page/introduccion) permite a las personas y empresas, pagar y cobrar electrónicamente usando sus propias cuentas corrientes o cuentas vista del banco, de manera fácil, rápida y segura. 

## Instalación

```bash
pip install pykhipu
```

## Uso

### Interfaz de bajo nivel

Iguala al API de Khipu en llamadas, ideal para portar código o en casos en que se busque más control sobre los resultados.

```python
from pykhipu.client import Client
from pykhipu import currency

client = Client(receiver_id='1234', secret='abcd')
payment = client.payments.post('test', currency.USD, 100)
print(payment.payment_url)
```
