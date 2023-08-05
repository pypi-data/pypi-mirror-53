# This file is part of barcodenumber. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

__all__ = ['ProductCode', 'ExpirationDate', 'Lot', 'SerialNumber']

SEPARATOR = '\x1d'


class Element(object):
    _ai = None
    _type = None
    _lenght = None

    @classmethod
    def extract(cls, num):
        # if 'ai' isn't at the beginning of the word
        if num.find(cls._ai):
            return
        _, remainder = num.split(cls._ai, 1)
        if cls._type == 'variable':
            if SEPARATOR in remainder:
                value, _ = remainder.split(SEPARATOR, 1)
                return value
        return remainder[:cls._lenght]


class ProductCode(Element):
    _ai = '01'
    _type = 'fixed'
    _lenght = 14


class ExpirationDate(Element):
    _ai = '17'
    _type = 'fixed'
    _lenght = 6


class Lot(Element):
    _ai = '10'
    _type = 'variable'
    _lenght = 20


class SerialNumber(Element):
    _ai = '21'
    _type = 'variable'
    _lenght = 20
