# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sitri', 'sitri.config', 'sitri.credentials']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.1,<6.0']

setup_kwargs = {
    'name': 'sitri',
    'version': '0.1.1',
    'description': 'Library for one endpoint config and credentials managment',
    'long_description': None,
    'author': 'Alexander Lavrov',
    'author_email': 'egnod@ya.ru',
    'url': 'https://github.com/Egnod/sitri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
