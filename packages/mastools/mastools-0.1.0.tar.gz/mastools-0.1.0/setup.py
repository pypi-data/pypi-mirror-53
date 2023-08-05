# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mastools', 'mastools.models']

package_data = \
{'': ['*'], 'mastools': ['scripts/*']}

install_requires = \
['psycopg2>=2.8,<3.0', 'sqlalchemy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['show-user-changes = '
                     'mastools.scripts.show_user_changes:handle_command_line']}

setup_kwargs = {
    'name': 'mastools',
    'version': '0.1.0',
    'description': "Tools for interacting directly with a Mastodon instance's database",
    'long_description': None,
    'author': 'Kirk Strauser',
    'author_email': 'kirk@strauser.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
