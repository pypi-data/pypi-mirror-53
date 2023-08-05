# commit message from test

[![Wheel Status](https://img.shields.io/pypi/wheel/cmft.svg)](https://pypi.python.org/pypi/cmft/)
[![Python versions](https://img.shields.io/pypi/pyversions/cmft.svg)](https://pypi.python.org/pypi/cmft/)
[![Latest Version](https://img.shields.io/pypi/v/cmft.svg)](https://pypi.python.org/pypi/cmft/)
[![License](https://img.shields.io/pypi/l/cmft.svg)](https://pypi.python.org/pypi/cmft/)
[![Build status](https://travis-ci.org/dryobates/commit-message-from-test.svg?branch=master)](https://travis-ci.org/dryobates/commit-message-from-test)
[![Coverage](https://coveralls.io/repos/dryobates/commit-message-from-test/badge.svg)](https://coveralls.io/r/dryobates/commit-message-from-test)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

commit-message-from-test (cmft in short) is tiny filter program to extract possible commit messages from changed files based on test names.

My motivation for writing it was to use with [tcr](https://github.com/dryobates/tcr). While coding, I don't like to be interrupted to enter some meaningful commit description, but at the same time I don't like completly useless "working". So I came out with something in the middle: commit descriptions based on test names.

Example usage with `tcr` and `fzf`:
```
$ tcr red `git diff HEAD | cmft | fzf --print-query | tail -n 1`
```