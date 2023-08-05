#!/usr/bin/env python
# coding: utf-8
'''Auxiliary models de Iydon.
'''
def __dir__() -> str:
	'''Return dir(self).
	'''
	return ['ParseRecord']


from collections import namedtuple


ParseRecord = namedtuple('ParseRecord', ('link', 'type'))
