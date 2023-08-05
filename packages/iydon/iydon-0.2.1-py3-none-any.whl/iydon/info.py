#!/usr/bin/env python
# coding: utf-8
'''Basic information de Iydon.
'''
__all__ = ['name_en', 'name_zh', 'emails', 'github', 'linkedin']
def __dir__() -> list: return __all__


from .config import name_en, name_zh, emails, github, linkedin
