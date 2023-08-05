#!/usr/bin/env python
# coding: utf-8
'''Configuration file de Iydon.
'''
__all__ = ['embed_colors', 'domain', 'subdomains']
def __dir__() -> list: return __all__


from .models import ParseRecord


# __main__
embed_colors = 'Linux'

# info
name_en = 'Iydon Liang'
name_zh = '梁钰栋'
emails = ('11711217@mail.sustech.edu.cn', )
github = 'https://github.com/Iydon'
linkedin = 'https://www.linkedin.com/in/钰栋-梁-0069ab185/'

# sites
domain = 'svegio.top'
subdomains = {
	'math': ParseRecord('10.20.6.187', 'A', False),
	'mma':  ParseRecord('sustech-mma.github.io', 'CNAME', True),
	'wic':  ParseRecord('mic-sd.github.io', 'CNAME', True),
	'www':  ParseRecord('iydon.github.io', 'CNAME', True)
}
