# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zita', 'zita.bin', 'zita.data', 'zita.serve', 'zita.train', 'zita.utils']

package_data = \
{'': ['*']}

install_requires = \
['ariadne>=0.6.0',
 'celery[redis]>=4.3.0,<5.0.0',
 'fastai>=1.0.57',
 'imagehash>=4.0',
 'orjson>=2.0.7,<3.0.0',
 'pyzmq>=18.1.0,<19.0.0',
 'redis>=3.3.8,<4.0.0',
 'uvicorn>=0.8.6']

setup_kwargs = {
    'name': 'zita',
    'version': '0.0.1.dev0',
    'description': 'Zillion Image Tagging App',
    'long_description': None,
    'author': 'Jesse Yang',
    'author_email': 'hello@yjc.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ktmud/zita',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
