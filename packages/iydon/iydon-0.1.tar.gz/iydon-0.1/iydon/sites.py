#!/usr/bin/env python
# coding: utf-8
'''Sites information de Iydon.
'''
def __dir__() -> str:
	'''Return dir(self).
	'''
	return ['get_all_links', 'get_full_link_by_subdomain']


from .config import domain, subdomains
from .models import ParseRecord
from .utils import typeassert, domain_join


@typeassert(str, bool)
def get_full_link_by_subdomain(subdomain, parse=False) -> [str, ParseRecord]:
	'''Get full link by subdomain.

	Argument
	=======
		subdomain: str
		parse: bool, whether to parse

	Return
	=======
		str or ParseRecord, full link
	'''
	assert subdomain in subdomains, '`{}` not in subdomains.'.format(subdomain)
	return subdomains[subdomain] if parse else domain_join((subdomain, domain))


@typeassert(bool)
def get_all_links(parse=False) -> list:
	'''Get all links de Iydon.

	Argument
	=======
		parse: bool, whether to parse

	Return
	=======
		list with all str or ParseRecord, full links
	'''
	if parse:
		return [subdomains[subdomain] for subdomain in subdomains]
	else:
		return [domain_join((subdomain, domain)) for subdomain in subdomains]
