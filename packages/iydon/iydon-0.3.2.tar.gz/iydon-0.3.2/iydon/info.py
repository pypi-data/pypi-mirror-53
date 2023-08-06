#!/usr/bin/env python
# coding: utf-8
'''Basic information de Iydon.
'''
info_keys = ['name_en', 'name_zh', 'emails', 'github', 'linkedin']
__all__ = info_keys + ['as_dict', 'as_namedtuple']
def __dir__() -> list: return __all__


from collections import namedtuple

from . import config
from .config import name_en, name_zh, emails, github, linkedin
from .utils import typeassert


@typeassert()
def as_dict() -> dict:
	'''Return information as dict.
	'''
	return {key:getattr(config, key) for key in info_keys}


Information = namedtuple('Information', info_keys)
@typeassert()
def as_namedtuple() -> namedtuple:
	'''Return information as namedtuple.
	'''
	args = [getattr(config, key) for key in info_keys]
	return Information(*args)
