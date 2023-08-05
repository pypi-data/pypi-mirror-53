#!/usr/bin/env python
# coding: utf-8
'''Initialize the namespace de Iydon.
'''
from . import sites


__all__ = ['sites']


def __dir__() -> list:
	'''Return dir(self).
	'''
	return __all__
