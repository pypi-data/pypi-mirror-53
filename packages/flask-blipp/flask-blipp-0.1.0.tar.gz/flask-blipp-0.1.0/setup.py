# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flask_blipp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flask-blipp',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'colinlcrawford',
    'author_email': 'ccolin84@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
