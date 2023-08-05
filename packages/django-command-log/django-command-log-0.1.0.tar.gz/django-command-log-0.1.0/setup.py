# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['command_log', 'command_log.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.1,<3.0', 'psycopg2-binary>=2.8,<3.0']

setup_kwargs = {
    'name': 'django-command-log',
    'version': '0.1.0',
    'description': 'Django management command auditing app',
    'long_description': '===================================\nDjango Management Command Audit Log\n===================================\n\nApp to enable simple auditing of Django management commands\n\nBackground\n----------\n\nThis app wraps the standad\n\n.. image:: screenshots/list-view.png\n\n.. image:: screenshots/detail-view.png\n   :scale: 100 %\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-managment-command-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
