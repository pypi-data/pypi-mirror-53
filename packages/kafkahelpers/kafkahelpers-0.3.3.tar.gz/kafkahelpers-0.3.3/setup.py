# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kafkahelpers']

package_data = \
{'': ['*']}

install_requires = \
['aiokafka>=0.5.0,<0.6.0', 'attrs>=18.2,<19.0', 'kafka-python>=1.4,<2.0']

setup_kwargs = {
    'name': 'kafkahelpers',
    'version': '0.3.3',
    'description': '',
    'long_description': None,
    'author': 'Jesse Jaggars',
    'author_email': 'jhjaggars@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
