#!/usr/bin/env python
# coding: utf-8
'''Basic information de Iydon.
'''
__all__ = ['name_en', 'name_zh', 'emails', 'github', 'linkedin', 'as_dict']
def __dir__() -> list: return __all__


from . import config
from .config import name_en, name_zh, emails, github, linkedin
from .utils import typeassert


@typeassert()
def as_dict() -> dict:
	'''Return information as dict.
	'''
	count = 5
	return {key:getattr(config, key) for key in __all__[:count]}
