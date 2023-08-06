# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poetryexample']

package_data = \
{'': ['*']}

install_requires = \
['FnF>=2.0,<3.0']

setup_kwargs = {
    'name': 'poetryexample',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Alan Bacon',
    'author_email': 'alan.bacon@bbc.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
