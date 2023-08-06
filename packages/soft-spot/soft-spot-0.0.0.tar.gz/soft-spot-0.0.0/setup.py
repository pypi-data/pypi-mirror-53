# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['soft_spot']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['sspot = soft_spot.__main__:cli']}

setup_kwargs = {
    'name': 'soft-spot',
    'version': '0.0.0',
    'description': 'Move to a land of Spot AWS instances',
    'long_description': '',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'url': 'https://github.com/fferegrino/soft-spot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
