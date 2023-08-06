# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poetryexample']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetryexample',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alan Bacon',
    'author_email': 'alan.bacon@bbc.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
