# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['djangorestcli', 'djangorestcli.controllers']

package_data = \
{'': ['*'], 'djangorestcli': ['templates/*']}

setup_kwargs = {
    'name': 'djangorestcli',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
