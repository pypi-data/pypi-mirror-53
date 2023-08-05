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
    'version': '0.1.1',
    'description': "Tools for interacting directly with a Mastodon instance's database",
    'long_description': '# mastools - Tools for interacting directly with a Mastodon instance\'s database\n\n## Installation\n\nIf you just want to use mastools and not work on the project itself: `pip install mastools`.\n\nIf you have [poetry](https://poetry.eustace.io) installed, run `poetry install`.\n\nIf not, use `pip` to install the dependencies mentioned in the `[tool.poetry.dependencies]` section of `pyproject.toml`.\n\n## Configuration\n\nMake a file named `~/.mastools/config.json` like:\n\n```json\n{\n    "host": "localhost",\n    "database": "mastodon",\n    "user": "mastodon",\n    "password": "0xdeadbeef"\n}\n```\n\nAll mastools components will use this database configuration.\n\n# The tools\n\n## show-user-changes\n\nShow any new, changed, or deleted accounts that mention URLs in their account\ninfo.\n\nThis is super common for spammers, who like to stuff their crummy website\'s info\ninto every single field possible. Suppose you run this hourly and email yourself\nthe results (which will usually be empty unless your instance is *very* busy).\nNow you can catch those "https://support-foo-corp/" spammers before they have a\nchance to post!\n\nFor example I run this from a cron job on my instance like:\n\n```\n10 * * * * /home/me/mastools/.venv/bin/show-user-changes\n```\n\nto get an hourly update of changes.\n\n# License\n\nDistributed under the terms of the `MIT`_ license, mastrools is free and open source software.\n\n# History\n\n- v0.1.0 - 2019-09-24: First release\n',
    'author': 'Kirk Strauser',
    'author_email': 'kirk@strauser.com',
    'url': 'https://github.com/freeradical-dot-zone/mastools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
