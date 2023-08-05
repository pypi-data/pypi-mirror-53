# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['iterchunk']

package_data = \
{'': ['*'], 'iterchunk': ['tests/*']}

setup_kwargs = {
    'name': 'iterchunk',
    'version': '0.0.2.dev0',
    'description': 'Split an iterable into chunks in Python.',
    'long_description': 'iterchunk\n=========\n.. image:: https://img.shields.io/travis/ianlini/iterchunk/master.svg\n   :target: https://travis-ci.org/ianlini/iterchunk\n.. image:: https://img.shields.io/pypi/v/iterchunk.svg\n   :target: https://pypi.python.org/pypi/iterchunk\n.. image:: https://img.shields.io/pypi/l/iterchunk.svg\n   :target: https://pypi.python.org/pypi/iterchunk\n.. image:: https://img.shields.io/github/stars/ianlini/iterchunk.svg?style=social\n   :target: https://github.com/ianlini/iterchunk\n\nSplit an iterable into chunks in Python.\n',
    'author': 'Ian Lin',
    'author_email': 'you@example.com',
    'url': 'https://github.com/ianlini/iterchunk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
