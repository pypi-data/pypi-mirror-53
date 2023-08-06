# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['testpoetrypypi']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['runtest = runtest:main',
                     'testpoetrypypi = testpoetrypypi:main']}

setup_kwargs = {
    'name': 'testpoetrypypi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeff',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
