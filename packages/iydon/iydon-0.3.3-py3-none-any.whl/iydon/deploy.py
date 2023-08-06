#!/usr/bin/env python
# coding: utf-8
'''Deployment de Iydon.
'''
__all__ = ['python_packages', 'overleaf']
def __dir__() -> list: return __all__


import pip
if hasattr(pip, 'main'):
	from pip import main as pip_
else:
	from pip._internal import main as pip_

from .config import py_pkgs_src, py_pkgs
from .config import overleaf_git, overleaf_man
from .sites import get_link_by_subdomain
from .utils import typeassert, doc_format, yes_or_no


@doc_format(set(py_pkgs.keys()))
@typeassert(bool, bool, bool, str)
def python_packages(ask=True, all_=False, user=False, source='', **kwargs):
	'''Install Python packages.

	Argument
	=======
		ask: bool, whether to use `yes_or_no`
		all_: bool, whether to install all packages
		user: bool, whether to use `--user`
		source: str, which PyPi website to use
		kwargs: in {}
	'''
	options = ['-i', source or py_pkgs_src]
	if user: options+=['--user']
	def install(pkgs:list):
		pip_(['install'] + pkgs + options)

	_locals = dict()

	for pkg in py_pkgs:
		_locals[pkg] = kwargs.get(pkg, None)
		if _locals[pkg] is not None:
			continue

		if ask:
			msg = pkg.replace('_', ' ').capitalize()
			_locals[pkg] = yes_or_no(msg=msg, empty=False)
		elif all_:
			_locals[pkg] = True

	for pkg in py_pkgs:
		if _locals[pkg]:
			install(py_pkgs[pkg])


@typeassert()
def overleaf():
	'''Manual for deploying Overleaf.
	'''
	print('GitHub:', overleaf_git)
	print('Manual:', get_link_by_subdomain('mma', full=True) + \
		overleaf_man)
