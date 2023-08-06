# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['yappa']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'click>=7.0,<8.0', 'python-slugify>=3.0,<4.0']

entry_points = \
{'console_scripts': ['yappa = yappa.cli:cli']}

setup_kwargs = {
    'name': 'yappa',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Mike',
    'author_email': 'mikhail.g.novikov@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
