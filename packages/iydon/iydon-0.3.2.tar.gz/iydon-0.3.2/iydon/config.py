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
py_pkgs_basic = ['bs4', 'faker', 'ipython', 'jupyter', 'tqdm']
py_pkgs_flask = ['alembic', 'bleach', 'blinker', 'click', 'dominate', 'flask', \
	'bootstrap-flask', 'flask-login', 'flask-mail', 'flask-migrate', 'flask-moment', \
	'flask-pagedown', 'flask-sqlalchemy', 'flask-wtf', 'html5lib', 'itsdangerous', 'jinja2', \
	'mako', 'markdown', 'markupsafe', 'python-dateutil', 'python-editor', 'six', 'sqlalchemy', \
	'visitor', 'webencodings', 'werkzeug', 'wtforms']
py_pkgs_research_basic = ['numpy', 'scipy', 'pandas', 'sympy', 'matplotlib', 'tushare', 'cython']
py_pkgs_research_dip = ['pillow']
py_pkgs_research_nlp = ['nltk', 'jieba']
py_pkgs_research_ml = ['sklearn']
py_pkgs_research_dl = ['torch', 'torchvision']

py_pkgs_src = 'https://pypi.mirrors.ustc.edu.cn/simple'


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
