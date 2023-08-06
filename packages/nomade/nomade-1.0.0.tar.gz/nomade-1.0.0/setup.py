# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nomade']

package_data = \
{'': ['*'], 'nomade': ['assets/*', 'constants/*']}

install_requires = \
['Jinja2==2.10.1',
 'click>=7.0,<8.0',
 'sqlalchemy>=1.3,<2.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['nomade = nomade.main:cli']}

setup_kwargs = {
    'name': 'nomade',
    'version': '1.0.0',
    'description': 'Migration Manager for Humans',
    'long_description': '<p align="center">\n    <img src="https://github.com/kelvins/nomade/blob/master/artwork/logo.svg" alt="Nomade Logo" title="Nomade Logo" width="250" height="150" />\n</p>\n\n<p align="center">\n    <a href="https://travis-ci.org/kelvins/nomade" alt="Build Status">\n        <img src="https://travis-ci.org/kelvins/nomade.svg?branch=master" />\n    </a>\n    <a href="https://coveralls.io/github/kelvins/nomade?branch=master" alt="Coverage Status">\n        <img src="https://coveralls.io/repos/github/kelvins/nomade/badge.svg?branch=master" />\n    </a>\n    <a href="https://pypi.org/project/nomade/" alt="PyPI Version">\n        <img src="https://img.shields.io/pypi/v/nomade.svg" />\n    </a>\n    <a href="https://www.python.org/downloads/release/python-370/" alt="Python Version">\n        <img src="https://img.shields.io/badge/python-3.7-blue.svg" />\n    </a>\n    <a href="https://github.com/psf/black" alt="Code Style">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" />\n    </a>\n    <a href="https://github.com/kelvins/nomade/blob/master/LICENSE" alt="License">\n        <img src="https://img.shields.io/badge/license-apache%202.0-blue.svg" />\n    </a>\n</p>\n\n> Python Migration Manager for Humans :camel:\n\nNomade is a simple migration manager tool that aims to be easy to integrate with any ORM (e.g. [SQLAlchemy](https://www.sqlalchemy.org/), [Peewee](http://docs.peewee-orm.com/en/latest/), [Pony](https://ponyorm.org/)) and database (e.g. [SQLite](https://www.sqlite.org/index.html), [MySQL](https://www.mysql.com/), [PostgreSQL](https://www.postgresql.org/)). It is basically a command-line interface (CLI) tool that manages migrations (Python files) by applying changes to the database schema and storing the current migration ID.\n\nThis tool was inspired by [alembic](https://alembic.sqlalchemy.org/en/latest/) (if you are using SQLAlchemy as ORM you should consider using alembic).\n\n> **Note**: this project is still under development so you may find bugs. If you find any bug, feel free to contribute by creating an issue and/or submitting a PR to fix it.\n\n## Installation\n\nUse [pip](https://pip.pypa.io/en/stable/installing/) to install Nomade:\n\n```bash\n$ pip install nomade\n```\n\n## Quick Start\n\nInitialize a **Nomade** project:\n\n```bash\n$ nomade init\n```\n\nIt will create the following project structure:\n\n```\n.\n├── nomade\n│   ├── template.py.j2\n│   └── migrations\n└── pyproject.toml\n```\n\nDefine **Nomade** settings in the `pyproject.toml` file, for example:\n\n```toml\n[tool.nomade]\nmigrations = "nomade/migrations"\ntemplate = "nomade/template.py.j2"\nconnection-string = "sqlite:///nomade.db"\ndate-format = "%d/%m/%Y"\nname-format = "{date}_{time}_{id}_{slug}"\n```\n\nThen, create your first migration:\n\n```bash\n$ nomade migrate "Create first table"\n```\n\nImplement the `upgrade` and `downgrade` functions in the migration file.\n\nThen apply the migration to the database:\n\n```bash\n$ nomade upgrade head\n```\n\nTo discover more **Nomade** features please read the documentation or call for help:\n\n```\n$ nomade --help\n\nUsage: nomade [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  current    Show the current migration.\n  downgrade  Downgrade migrations.\n  history    Show migrations history.\n  init       Init a Nomade project.\n  migrate    Create a new migration.\n  stamp      Stamp a specific migration to the database.\n  upgrade    Upgrade migrations.\n  version    Show Nomade version.\n```\n\n## How to Contribute\n\n- Check for open issues or open a fresh one to start a discussion around a feature idea or a bug.\n- Become more familiar with the project by reading the [Contributor\'s Guide](CONTRIBUTING.rst).\n',
    'author': 'Kelvin S. do Prado',
    'author_email': 'kelvinpfw@gmail.com',
    'url': 'https://github.com/kelvins/nomade',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
