#!/usr/bin/env python
# coding: utf-8
'''Auxiliary file de Iydon.
'''
def __dir__() -> str:
	'''Return dir(self).
	'''
	return ['typeassert', 'domain_join']


from inspect import signature
from functools import wraps
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


@typeassert(Iterable)
def domain_join(domains):
	'''Join domain and subdomain.

	Argument
	=======
		domains: Iterable[str]
	'''
	# If in optimized mode, disable type checking
	if __debug__:
		for value in domains:
			assert isinstance(value, str), 'Argument must be Iterable with all str.'

	return '.'.join(domains)
