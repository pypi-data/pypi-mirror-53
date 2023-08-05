#!/usr/bin/env python
# coding: utf-8
'''Auxiliary file de Iydon.
'''
__all__ = ['typeassert', 'domain_join', 'json_loads_online']
def __dir__() -> list: return __all__


from inspect import signature
from functools import wraps
from json import loads
from requests import get
from typing import Iterable


def typeassert(*t_args, **t_kwargs):
	'''Enforce type check on function using decorator.

	Todo
	=======
	Check the type of return value.

	References
	=======
	(Python Cookbook)[https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p07_enforcing_type_check_on_function_using_decorator.html]
	'''
	def decorate(func):
		# If in optimized mode, disable type checking
		if not __debug__:
			return func

		# Map function argument names to supplied types
		σ = signature(func)
		bound_types = σ.bind_partial(*t_args, **t_kwargs).arguments

		@wraps(func)
		def wrapper(*args, **kwargs):
			bound_values = σ.bind(*args, **kwargs)
			# Enforce type assertions across supplied arguments
			for name, value in bound_values.arguments.items():
				if name in bound_types:
					if not isinstance(value, bound_types[name]):
						raise TypeError(
							'Argument `{}` must be {}.'.format(name, bound_types[name])
						)
			return func(*args, **kwargs)
		return wrapper
	return decorate


@typeassert(Iterable, bool, bool)
def domain_join(domains, full=False, https=False):
	'''Join domain and subdomain.

	Argument
	=======
		domains: Iterable[str]
		full: bool, whether to return full link
		https: bool, whether to use HTTP Secure
	'''
	# If in optimized mode, disable type checking
	if __debug__:
		for value in domains:
			assert isinstance(value, str), 'Argument must be Iterable with all str.'

	if full:
		return ('https://' if https else 'http://') + '.'.join(domains)
	else:
		return '.'.join(domains)


@typeassert(str)
def json_loads_online(url):
	'''Deserialize json data from `url`.

	Todo
	=======
	[GitHub API](https://api.github.com/)

	Argument
	=======
		url: str
	'''
	response = get(url)
	return loads(response.text)
