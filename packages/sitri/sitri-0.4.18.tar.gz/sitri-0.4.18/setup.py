# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sitri', 'sitri.config', 'sitri.contrib', 'sitri.credentials']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sitri',
    'version': '0.4.18',
    'description': 'Library for one endpoint config and credentials managment',
    'long_description': '\n<p align="center">\n  <a href="https://github.com/lemegetonx/sitri">\n    <img src="docs/_static/logo.gif">\n  </a>\n  <h1 align="center">\n    Sitri Configuration Library\n  </h1>\n</p>\n\nSitri - library for managing authorization and configuration data from a single object with possibly different or identical providers\n\n#  Installation\n\n```bash\npoetry add sitri\n```\n\nor\n```bash\npip3 install sitri\n```\n\n# Basics with SystemProvider\n\n```python\nfrom sitri.contrib.system import SystemCredentialProvider, SystemConfigProvider\nfrom sitri import Sitri\n\nconf = Sitri(config_provider=SystemConfigProvider(prefix="basics"),\n             credential_provider=SystemCredentialProvider(prefix="basics"))\n```\nSystem provider use system environment for get config and credential data. For unique sitri lookup to "namespace" by prefix.\n\nExample:\n\n*In console:*\n```bash\nexport BASICS_NAME=Huey\n```\n\n*In code:*\n```python\nname = conf.get_config("name")\nprint(name)  # output: Huey\n```\n\n#  Docs\nRead base API references and other part documentation on https://sitri.readthedocs.io/\n',
    'author': 'Alexander Lavrov',
    'author_email': 'egnod@ya.ru',
    'url': 'https://github.com/Egnod/sitri',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
