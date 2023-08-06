# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bookery',
 'bookery.common',
 'bookery.models',
 'bookery.persistence',
 'bookery.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PySide2>=5.13,<6.0', 'SQLAlchemy>=1.3,<2.0']

setup_kwargs = {
    'name': 'bookery',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Donghyeon Kim',
    'author_email': '0916dhkim@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
