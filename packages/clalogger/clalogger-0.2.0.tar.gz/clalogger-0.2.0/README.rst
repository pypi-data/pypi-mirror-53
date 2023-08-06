clalogger - Python logging from class point of view with easy configuration
===========================================================================

See doc/index.rst

This project provides a python ClaLogger class which have to be inherited and
provides logging which uses loggers based on the class name.

It also provides easy configuration features, via a `configfile` file.

Installation and requirements
-----------------------------

This requires `python >= 3.7`. It can be simply installed via `pip install
clalogger`.

Development also needs `pipenv`. You have to `cd` to the package directory and
run `pipenv shell`, followed by `pipenv install -d`. Development environment
can then easily be setup using `python setup.py develop`.

Building the documentation also requires `sphinx`. It is automatically
installed via `pipenv install d-`.

Contacts, issues and copyright
------------------------------

The author can be contacted on: michael_AT_hooreman_DOT_be

Issues can be described on the github project: https://github.com/mhooreman/clalogger

Copyright (C) 2019 Michaël Hooreman
Released under the terms of the MIT license, see LICENSE.
