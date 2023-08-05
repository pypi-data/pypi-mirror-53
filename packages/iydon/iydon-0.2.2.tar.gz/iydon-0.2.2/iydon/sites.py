#!/usr/bin/env python
# coding: utf-8
'''Sites information de Iydon.
'''
__all__ = ['get_all_links', 'get_link_by_subdomain']
def __dir__() -> list: return __all__


from .config import domain, subdomains
from .models import ParseRecord
from .utils import typeassert, domain_join


@typeassert(str, bool, bool)
def get_link_by_subdomain(subdomain, parse=False, full=False) -> [str, ParseRecord]:
	'''Get link by subdomain.

	Argument
	=======
		subdomain: str
		parse: bool, whether to parse
		full: bool, whether to return full link

	Return
	=======
		str or ParseRecord, full link
	'''
	assert subdomain in subdomains, '`{}` not in subdomains.'.format(subdomain)
	return subdomains[subdomain] if parse else \
		domain_join((subdomain, domain), full, subdomains[subdomain].https)


@typeassert(bool, bool)
def get_all_links(parse=False, full=False) -> list:
	'''Get all links de Iydon.

	Argument
	=======
		parse: bool, whether to parse

	Return
	=======
		list with all str or ParseRecord, full links
	'''
	return [get_link_by_subdomain(subdomain, parse, full) \
		for subdomain in subdomains]
