#!/usr/bin/env python
# coding: utf-8
'''Configuration file de Iydon.
'''
def __dir__() -> str:
	'''Return dir(self).
	'''
	return ['domain', 'subdomains']


from .models import ParseRecord


# __main__
embed_colors = 'Linux'

# sites
domain = 'svegio.top'
subdomains = {
	'math': ParseRecord('10.20.6.187', 'A'),
	'mma':  ParseRecord('sustech-mma.github.io', 'CNAME'),
	'wic':  ParseRecord('mic-sd.github.io', 'CNAME'),
	'www':  ParseRecord('iydon.github.io', 'CNAME')
}
