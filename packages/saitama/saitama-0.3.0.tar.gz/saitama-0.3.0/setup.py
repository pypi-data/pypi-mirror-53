# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['saitama', 'saitama.queries']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.8,<3.0', 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['punch = saitama.punch:main']}

setup_kwargs = {
    'name': 'saitama',
    'version': '0.3.0',
    'description': 'A python toolset to manage postgres migrations and testing',
    'long_description': '<p align="center">\n    <a href="https://github.com/ambv/black">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n    </a>\n</p>\n',
    'author': 'spapanik',
    'author_email': 'spapanik21@gmail.com',
    'url': 'https://github.com/spapanik/saitama',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
