# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['asyncify']
install_requires = \
['pytest-asyncio>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'asyncify',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
