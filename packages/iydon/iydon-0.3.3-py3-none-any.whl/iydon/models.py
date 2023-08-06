#!/usr/bin/env python
# coding: utf-8
'''Auxiliary models de Iydon.
'''
__all__ = ['ParseRecord']
def __dir__() -> list: return __all__


from collections import namedtuple


ParseRecord = namedtuple('ParseRecord', ('link', 'type', 'https'))
