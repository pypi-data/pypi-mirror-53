#!/usr/bin/env python
# coding: utf-8
'''Initialize the namespace de Iydon.
'''
__all__ = ['sites', 'info']
def __dir__() -> list: return __all__


from . import info
from . import sites
