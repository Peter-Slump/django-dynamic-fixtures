# django-dynamic-fixtures


Django: **1.11 2.2 3.0**  
Python: **3.4, 3.5, 3.6, 3.7, 3.8**

[![Build Status](https://travis-ci.org/Peter-Slump/django-dynamic-fixtures.svg?branch=master)](https://travis-ci.org/Peter-Slump/django-dynamic-fixtures)
[![Documentation Status](https://readthedocs.org/projects/django-dynamic-fixtures/badge/?version=latest)](http://django-dynamic-fixtures.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Peter-Slump/django-dynamic-fixtures/branch/master/graph/badge.svg)](https://codecov.io/gh/Peter-Slump/django-dynamic-fixtures)
[![Maintainability](https://api.codeclimate.com/v1/badges/2b19eae6a4aaa8cfa03b/maintainability)](https://codeclimate.com/github/Peter-Slump/django-dynamic-fixtures/maintainability)

[![PyPI](https://img.shields.io/pypi/l/django-dynamic-fixtures.svg)](https://pypi.python.org/pypi/django-dynamic-fixtures)
[![PyPI](https://img.shields.io/pypi/v/django-dynamic-fixtures.svg)](https://pypi.python.org/pypi/django-dynamic-fixtures)
[![PyPI](https://img.shields.io/pypi/wheel/django-dynamic-fixtures.svg)](https://pypi.python.org/pypi/django-dynamic-fixtures)


A Django app to install dynamic fixtures.

[Read documentation](http://django-dynamic-fixtures.readthedocs.io/en/latest/)

## Development

Install development environment:

```bash
$ make install-python
```

Run all unittests*:

```bash
$ pip install --upgrade distribute
$ python setup.py test
```

\* Make sure that the `tests` folder isn't added to the sys path.

### Writing documentation

Install dependencies: 

```bash
$ make install-python
```

Docs can be written using Sphinx in `docs/source`.
To run auto-build of the docs:

```
$ cd docs
$ make watch
```
