# -*- coding: utf-8 -*-
class Receivers(object):
    ENDPOINT = '/receivers'

    def __init__(self, client):
        self.client = client

    def post(self, data):
        """
        Crear una nueva cuenta de cobro asociada a un integrador. Necesita datos
        de la cuenta de usuario asociada, datos de facturación y datos de
        contacto.
        """
        response = self.client.make_request('POST', self.ENDPOINT, data=data)
        return ReceiversCreateResponse.from_response(response)
