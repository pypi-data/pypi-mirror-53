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
    'version': '0.4.0',
    'description': 'A little CLI tool to record, categorize and display quotes',
    'long_description': '# termquotes\n\nA little CLI tool to record, categorize and display quotes.\n\n## Install\n\n`pip install --user termquotes`\n\n## Usage\n\n`termquotes --help`\n\n#### Shell\n\nIn `.zshrc`\n\n`termquotes get | cowsay -f vader | lolcat`\n\n```\n ________________________________________\n/ APIs should be easy to use and hard to \\\n\\ misuse. -- Josh Bloch                  /\n ----------------------------------------\n        \\    ,-^-.\n         \\   !oYo!\n          \\ /./=\\.\\______\n               ##        )\\/\\\n                ||-----w||\n                ||      ||\n\n               Cowth Vader\n```\n',
    'author': 'Titus Soporan',
    'author_email': 'titus@tsoporan.com',
    'url': 'https://github.com/tsoporan/termquotes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
