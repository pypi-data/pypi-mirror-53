# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['quantrocket_utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.2,<0.16.0',
 'colorama>=0.4.1,<0.5.0',
 'ib-trading-calendars>=0.1.2,<0.2.0',
 'termcolor>=1.1,<2.0',
 'trading-calendars>=1.10,<2.0']

setup_kwargs = {
    'name': 'quantrocket-utils',
    'version': '0.1.0',
    'description': 'Utility methods for common tasks in QuantRocket.',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
