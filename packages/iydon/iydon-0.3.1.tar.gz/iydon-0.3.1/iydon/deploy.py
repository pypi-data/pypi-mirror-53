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


@typeassert(bool, bool, bool, bool, bool, bool, bool, bool, bool, str)
def py_pkgs(ask=True, all_=False, basic=False, flask=False, research=False, \
	digit_image_processing=False, natural_language_processing=False, machine_learning=False, \
	deep_learning=False, source=''):
	'''Install Python packages.

	Argument
	=======
		ask: bool, whether to use `yes_or_no`
		all_: bool, whether to install all packages
	'''
	source = source or py_pkgs_src
	def install(pkgs:list):
		pip_(['install'] + pkgs + ['-i', source])
	
	if ask:
		basic = yes_or_no(msg='Whether to install basic', empty=False)
		flask = yes_or_no(msg='Whether to install flask', empty=False)
		research = yes_or_no(msg='Whether to install research packages', empty=False)
		digit_image_processing = yes_or_no(msg='Whether to install image processing packages', empty=False)
		natural_language_processing = yes_or_no(msg='Whether to install NLP packages', empty=False)
		machine_learning = yes_or_no(msg='Whether to install machine learning packages', empty=False)
		deep_learning = yes_or_no(msg='Whether to install deep learning packages', empty=False)
	elif all_:
		basic = flask = research = digit_image_processing = True
		natural_language_processing = machine_learning = deep_learning = True

	if basic: install(py_pkgs_basic)
	if flask: install(py_pkgs_flask)
	if research: install(py_pkgs_research_basic)
	if digit_image_processing: install(py_pkgs_research_dip)
	if natural_language_processing: install(py_pkgs_research_nlp)
	if machine_learning: install(py_pkgs_research_ml)
	if deep_learning: install(py_pkgs_research_dl)
