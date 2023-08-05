# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tiktok_bot', 'tiktok_bot.api', 'tiktok_bot.bot', 'tiktok_bot.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.7.2,<0.8.0',
 'loguru>=0.3.2,<0.4.0',
 'pydantic>=0.32.2,<0.33.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tiktok-bot',
    'version': '0.3.0',
    'description': 'Tik Tok API',
    'long_description': None,
    'author': 'Evgeny Kemerov',
    'author_email': 'eskemerov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
