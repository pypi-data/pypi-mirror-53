#!/usr/bin/env python
# coding: utf-8
'''Deployment de Iydon.
'''
__all__ = ['py_pkgs']
def __dir__() -> list: return __all__


import pip
if hasattr(pip, 'main'):
	from pip import main as pip_
else:
	from pip._internal import main as pip_

from .config import py_pkgs_basic, py_pkgs_flask, py_pkgs_research_basic, \
	py_pkgs_research_dip, py_pkgs_research_nlp, py_pkgs_research_ml, py_pkgs_research_dl, \
	py_pkgs_src
from .utils import typeassert, yes_or_no


@typeassert(bool, bool, bool, str)
def py_pkgs(ask=True, all_=False, user=False, source='', **kwargs):
	'''Install Python packages.

	Argument
	=======
		ask: bool, whether to use `yes_or_no`
		all_: bool, whether to install all packages
		user: bool, whether to use `--user`
		source: str, which PyPi website to use
	'''
	options = ['-i', source or py_pkgs_src]
	if user: options+=['--user']
	def install(pkgs:list):
		pip_(['install'] + pkgs + options)

	basic = kwargs.get('basic', False)
	flask = kwargs.get('flask', False)
	research = kwargs.get('research', False)
	digit_image_processing = kwargs.get('digit_image_processing', False)
	natural_language_processing = kwargs.get('natural_language_processing', False)
	machine_learning = kwargs.get('machine_learning', False)
	deep_learning = kwargs.get('deep_learning', False)
	
	if ask:
		basic = yes_or_no(msg='Basic packages', empty=False)
		flask = yes_or_no(msg='Flask', empty=False)
		research = yes_or_no(msg='Research basic packages', empty=False)
		digit_image_processing = yes_or_no(msg='Image processing packages', empty=False)
		natural_language_processing = yes_or_no(msg='NLP packages', empty=False)
		machine_learning = yes_or_no(msg='Machine learning packages', empty=False)
		deep_learning = yes_or_no(msg='Deep learning packages', empty=False)
	elif all_:
		basic = flask = research = digit_image_processing = \
			natural_language_processing = machine_learning = deep_learning = True

	if basic: install(py_pkgs_basic)
	if flask: install(py_pkgs_flask)
	if research: install(py_pkgs_research_basic)
	if digit_image_processing: install(py_pkgs_research_dip)
	if natural_language_processing: install(py_pkgs_research_nlp)
	if machine_learning: install(py_pkgs_research_ml)
	if deep_learning: install(py_pkgs_research_dl)
