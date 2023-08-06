# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keios_dynabuffers_rhea']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'keios-dynabuffers-rhea',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'fridayy',
    'author_email': 'benjamin.krenn@leftshift.one',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
