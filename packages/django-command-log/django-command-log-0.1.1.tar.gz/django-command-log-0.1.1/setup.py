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
    'version': '0.1.1',
    'description': 'Django management command auditing app',
    'long_description': '# Django Management Command Audit Log\n\nApp to enable simple auditing of Django management commands\n\n## Background\n\nThis app wraps the standad Django management command base class to record the running of a command. It logs the name of the command, start and end time, and the output (if any). If the command fails with a Python exception, the error message is added to the record, and the exception itself is logged using `logging.exception`.\n\n![Screenshot of admin list view](https://github.com/yunojuno/django-managment-command-log/blob/master/screenshots/detail-view.png")\n\n![Screenshot of admin detail view](https://github.com/yunojuno/django-managment-command-log/blob/master/screenshots/detail-view.png")\n\nSee the `test_command` and `test_transaction_command` for examples.\n\n## TODO\n\nDocumentation.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-managment-command-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
