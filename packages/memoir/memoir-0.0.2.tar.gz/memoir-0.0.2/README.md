memoir
======

[![](https://travis-ci.org/lycantropos/memoir.svg?branch=master)](https://travis-ci.org/lycantropos/memoir "Travis CI")
[![](https://ci.appveyor.com/api/projects/status/github/lycantropos/memoir?branch=master&svg=true)](https://ci.appveyor.com/project/lycantropos/memoir "AppVeyor")
[![](https://codecov.io/gh/lycantropos/memoir/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/memoir "Codecov")
[![](https://img.shields.io/github/license/lycantropos/memoir.svg)](https://github.com/lycantropos/memoir/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/memoir.svg)](https://badge.fury.io/py/memoir "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade memoir
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade memoir
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/memoir.git
cd memoir
```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Usage
-----

Let's suppose we are defining a class 
with expensive read-only [`property`](https://docs.python.org/library/functions.html#property) 
which can be calculated once and reused afterwards.

Common way of solving this is by introducing private'ish attribute like
```python
>>> class Example:
...     @property
...     def expensive_property(self):
...         try:
...             result = self._expensive_property
...         except AttributeError:
...             result = do_expensive_calculations(...)
...             self._expensive_property = result
...         return result

```
this works fine, but each such property

- introduces an extra attribute,
- requires a lot of boilerplate code.

If we have

- [weakly-referencable](https://docs.python.org/library/weakref.html) 
(which is by default if not suppressed explicitly, 
e.g. by using [`__slots__` class variable](https://docs.python.org/reference/datamodel.html#slots)),
- [hashable](https://docs.python.org/glossary.html#term-hashable)

class we can implement it like
```python
>>> from memoir import cached
>>> class Example:
...     @cached.property_
...     def expensive_property(self):
...         return do_expensive_calculations(...)

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose --tag release
```

Bump version
```bash
bump2version --verbose --tag release
```

This will set version to `major.minor.patch` and add `Git` tag.

#### Notes

To avoid inconsistency between branches and pull requests,
bumping version should be merged into `master` branch as separate pull
request.

### Running tests

Plain:
- with `CPython`
  ```bash
  python setup.py test
  ```
- with `PyPy`
  ```bash
  pypy setup.py test
  ```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
