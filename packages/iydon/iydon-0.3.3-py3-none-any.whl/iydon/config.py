#!/usr/bin/env python
# coding: utf-8
'''Configuration file de Iydon.
'''
__all__ = ['embed_colors', 'domain', 'subdomains']
def __dir__() -> list: return __all__


from .models import ParseRecord


# __main__
embed_colors = 'Linux'


# deploy
py_pkgs_src = 'https://pypi.mirrors.ustc.edu.cn/simple'
py_pkgs = {
	'basic': ['bs4', 'faker', 'ipython', 'jupyter', 'tqdm'],
	'flask': ['alembic', 'bleach', 'blinker', 'click', 'dominate', 'flask', \
		'bootstrap-flask', 'flask-login', 'flask-mail', 'flask-migrate', 'flask-moment', \
		'flask-pagedown', 'flask-sqlalchemy', 'flask-wtf', 'html5lib', 'itsdangerous', 'jinja2', \
		'mako', 'markdown', 'markupsafe', 'python-dateutil', 'python-editor', 'six', 'sqlalchemy', \
		'visitor', 'webencodings', 'werkzeug', 'wtforms'],
	'research': ['numpy', 'scipy', 'pandas', 'sympy', 'matplotlib', 'tushare', 'cython'],
	'digit_image_processing': ['pillow'],
	'natural_language_processing': ['nltk', 'jieba'],
	'machine_learning': ['sklearn'],
	'deep_learning': ['torch', 'torchvision']
}

overleaf_git = 'https://github.com/overleaf/overleaf'
overleaf_man = '/2018/10/ShareLaTeX-LaTeX/'


# info
name_en = 'Iydon Liang'
name_zh = '梁钰栋'
emails = ('11711217@mail.sustech.edu.cn', 'liangiydon@gmail.com')
github = 'https://github.com/Iydon'
linkedin = 'https://www.linkedin.com/in/钰栋-梁-0069ab185/'


# sites
domain = 'svegio.top'
subdomains = {
	'math': ParseRecord('10.20.6.187', 'A', False),
	'mma':  ParseRecord('sustech-mma.github.io', 'CNAME', True),
	'wic':  ParseRecord('mic-sd.github.io', 'CNAME', True),
	'www':  ParseRecord('iydon.github.io', 'CNAME', True)
}
