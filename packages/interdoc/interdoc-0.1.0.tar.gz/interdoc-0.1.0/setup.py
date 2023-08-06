# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['interdoc']

package_data = \
{'': ['*']}

install_requires = \
['attrs==19.1.0', 'click==7.0']

entry_points = \
{'console_scripts': ['interdoc = interdoc.cli:cli']}

setup_kwargs = {
    'name': 'interdoc',
    'version': '0.1.0',
    'description': '',
    'long_description': '========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - tests\n      - | |travis|\n        |\n    * - package\n      - | |version| |wheel| |supported-versions| |supported-implementations|\n        | |commits-since|\n\n.. |docs| image:: https://readthedocs.org/projects/interdoc/badge/?style=flat\n    :target: https://readthedocs.org/projects/interdoc\n    :alt: Documentation Status\n\n\n.. |travis| image:: https://travis-ci.org/metatooling/interdoc.svg?branch=master\n    :alt: Travis-CI Build Status\n    :target: https://travis-ci.org/metatooling/interdoc\n\n.. |version| image:: https://img.shields.io/pypi/v/interdoc.svg\n    :alt: PyPI Package latest release\n    :target: https://pypi.org/pypi/interdoc\n\n.. |commits-since| image:: https://img.shields.io/github/commits-since/metatooling/interdoc/v0.1.0.svg\n    :alt: Commits since latest release\n    :target: https://github.com/metatooling/interdoc/compare/v0.1.0...master\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/interdoc.svg\n    :alt: PyPI Wheel\n    :target: https://pypi.org/pypi/interdoc\n\n.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/interdoc.svg\n    :alt: Supported versions\n    :target: https://pypi.org/pypi/interdoc\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/interdoc.svg\n    :alt: Supported implementations\n    :target: https://pypi.org/pypi/interdoc\n\n\n.. end-badges\n\nInteractive docs\n\n* Free software: MIT License\n\nInstallation\n============\n\n::\n\n    pip install interdoc\n\nDocumentation\n=============\n\n\nhttps://interdoc.readthedocs.io/\n\n\nDevelopment\n===========\n\nTo run the all tests run::\n\n    tox\n\nNote, to combine the coverage data from all the tox environments run:\n\n.. list-table::\n    :widths: 10 90\n    :stub-columns: 1\n\n    - - Windows\n      - ::\n\n            set PYTEST_ADDOPTS=--cov-append\n            tox\n\n    - - Other\n      - ::\n\n            PYTEST_ADDOPTS=--cov-append tox\n',
    'author': 'Interdoc contributors',
    'author_email': 'metatooling@users.noreply.github.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
