# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cmft']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cmft = cmft.__main__:main']}

setup_kwargs = {
    'name': 'cmft',
    'version': '0.1.0',
    'description': '',
    'long_description': '# commit message from test\n\n[![Wheel Status](https://img.shields.io/pypi/wheel/cmft.svg)](https://pypi.python.org/pypi/cmft/)\n[![Python versions](https://img.shields.io/pypi/pyversions/cmft.svg)](https://pypi.python.org/pypi/cmft/)\n[![Latest Version](https://img.shields.io/pypi/v/cmft.svg)](https://pypi.python.org/pypi/cmft/)\n[![License](https://img.shields.io/pypi/l/cmft.svg)](https://pypi.python.org/pypi/cmft/)\n[![Build status](https://travis-ci.org/dryobates/commit-message-from-test.svg?branch=master)](https://travis-ci.org/dryobates/commit-message-from-test)\n[![Coverage](https://coveralls.io/repos/dryobates/commit-message-from-test/badge.svg)](https://coveralls.io/r/dryobates/commit-message-from-test)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\ncommit-message-from-test (cmft in short) is tiny filter program to extract possible commit messages from changed files based on test names.\n\nMy motivation for writing it was to use with [tcr](https://github.com/dryobates/tcr). While coding, I don\'t like to be interrupted to enter some meaningful commit description, but at the same time I don\'t like completly useless "working". So I came out with something in the middle: commit descriptions based on test names.\n\nExample usage with `tcr` and `fzf`:\n```\n$ tcr red `git diff HEAD | cmft | fzf --print-query | tail -n 1`\n```',
    'author': 'dryobates',
    'author_email': 'jakub.stolarski@gmail.com',
    'url': 'https://github.com/dryobates/commit-message-from-test',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
