# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['crawl_classic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crawl-classic',
    'version': '0.1.2',
    'description': 'Random tables for Dungeon Crawl Classics RPG.',
    'long_description': '# Crawl Classics RPG\n\nRandom tables for Dungeon Crawl Classics RPG.\n',
    'author': 'Seth Woodworth',
    'author_email': 'seth@sethish.com',
    'url': 'https://github.com/sethwoodworth/crawl-classic',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
