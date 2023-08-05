# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiohttp_scraper', 'aiohttp_scraper.scripts']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.6.1,<4.0.0',
 'aioredis>=1.2.0,<2.0.0',
 'tldextract>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'aiohttp-scraper',
    'version': '0.1.4',
    'description': 'An asyncronous HTTP client built for web scraping.',
    'long_description': None,
    'author': 'Johannes Gontrum',
    'author_email': 'j@gontrum.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
