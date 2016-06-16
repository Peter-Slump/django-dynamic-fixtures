# django-dynamic-fixtures


Django: **1.7, 1.8**  
Python: **2.7, 3.3, 3.4**  

[![Build Status](https://travis-ci.org/Peter-Slump/django-dynamic-fixtures.svg?branch=master)](https://travis-ci.org/Peter-Slump/django-dynamic-fixtures)
[![Documentation Status](https://readthedocs.org/projects/django-dynamic-fixtures/badge/?version=latest)](http://django-dynamic-fixtures.readthedocs.io/en/latest/?badge=latest)

A Django app to install dynamic fixtures.

[Documentation](http://django-dynamic-fixtures.readthedocs.io/en/latest/)

## Development

Install development environment:

```bash
$ make install-python
```

Run all unittests*:

```bash
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
