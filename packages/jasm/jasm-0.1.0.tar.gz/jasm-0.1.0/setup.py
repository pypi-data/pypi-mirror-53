# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['jasm']
setup_kwargs = {
    'name': 'jasm',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
