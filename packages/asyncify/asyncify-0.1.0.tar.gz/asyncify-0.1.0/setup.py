# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['asyncify']
setup_kwargs = {
    'name': 'asyncify',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
