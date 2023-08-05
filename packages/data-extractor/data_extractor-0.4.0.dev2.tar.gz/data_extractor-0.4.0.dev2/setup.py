# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['data_extractor']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.0.3,<2.0.0',
 'jsonpath-rw-ext>=1.2,<2.0',
 'jsonpath-rw>=1.4.0,<2.0.0',
 'lxml>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'data-extractor',
    'version': '0.4.0.dev2',
    'description': 'Combine XPath, CSS Selector and JSONPath for Web data extracting.',
    'long_description': '[![license](https://img.shields.io/github/license/linw1995/data_extractor.svg)](https://github.com/linw1995/data_extractor/blob/master/LICENSE)\n[![Pypi Status](https://img.shields.io/pypi/status/data_extractor.svg)](https://pypi.org/project/data_extractor)\n[![Python version](https://img.shields.io/pypi/pyversions/data_extractor.svg)](https://pypi.org/project/data_extractor)\n[![Package version](https://img.shields.io/pypi/v/data_extractor.svg)](https://pypi.org/project/data_extractor)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/data-extractor.svg)](https://pypi.org/project/data_extractor)\n[![GitHub last commit](https://img.shields.io/github/last-commit/linw1995/data_extractor.svg)](https://github.com/linw1995/data_extractor)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Build Status](https://travis-ci.org/linw1995/data_extractor.svg?branch=master)](https://travis-ci.org/linw1995/data_extractor)\n[![codecov](https://codecov.io/gh/linw1995/data_extractor/branch/master/graph/badge.svg)](https://codecov.io/gh/linw1995/data_extractor)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-brightgreen.svg)](https://linw1995.com/data_extractor)\n\n# Data Extractor\n\nCombine **XPath**, **CSS Selector** and **JSONPath** for Web data extracting.\n',
    'author': 'linw1995',
    'author_email': 'linw1995@icloud.com',
    'url': 'https://github.com/linw1995/data_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
