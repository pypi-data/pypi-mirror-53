# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['termquotes']

package_data = \
{'': ['*'], 'termquotes': ['data/*']}

install_requires = \
['click>=7.0,<8.0', 'colorama>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['termquotes = termquotes.console:cli']}

setup_kwargs = {
    'name': 'termquotes',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Titus Soporan',
    'author_email': 'titus@tsoporan.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
