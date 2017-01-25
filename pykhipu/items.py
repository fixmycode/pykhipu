# -*- coding: utf-8 -*-
class BankItem(object):
    def __init__(self, bank_id, name, message, min_amount, bank_type, parent):
        self._bank_id = bank_id
        self._name = name
        self._message = message
        self._min_amount = min_amount
        self._type = bank_type
        self._parent = parent

    @classmethod
    def from_data(cls, data):
        """
        Constructor que permite obtener una instancia de BankItem a partir de un
        diccionario de datos.
        """
        return cls(data.get('bank_id'), data.get('name'), data.get('message'),
            data.get('min_amount'), data.get('type'), data.get('parent'))

    @property
    def bank_id(self):
        """
        Identificador del banco
        """
        return self._bank_id

    @property
    def name(self):
        """
        Nombre del banco
        """
        return self._name

    @property
    def message(self):
        """
        Mensaje con particularidades del banco
        """
        return self._message

    @property
    def min_amount(self):
        """
        Monto mínimo que acepta el banco en un pago
        """
        return self._min_amount

    @property
    def bank_type(self):
        """
        Tipo de banco. Nombre en el API: type
        """
        return self._type

    @property
    def parent(self):
        """
        Identificador del banco padre (si un banco tiene banca personas y
        empresas, el primero será el padre del segundo)
        """
        return self._parent


class ErrorItem(object):
    def __init__(self, field, message):
        self._field = field
        self._message = message

    @classmethod
    def from_data(cls, data):
        return cls(data.get('field'), data.get('message'))

    @property
    def field(self):
        """
        Campo que tiene el error de validación
        """
        return self._field

    @property
    def message(self):
        """
        Motivo del error de validación
        """
        return self._message
