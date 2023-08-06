# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['punctual']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'colorama>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pcl = punctual:cli.cli']}

setup_kwargs = {
    'name': 'punctual',
    'version': '0.1.0',
    'description': 'Clean and simple docfile management with a lot of flexibility',
    'long_description': None,
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
