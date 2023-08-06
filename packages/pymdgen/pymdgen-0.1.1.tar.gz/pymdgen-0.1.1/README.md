[![PyPI](https://img.shields.io/pypi/v/pymdgen.svg?maxAge=3600)](https://pypi.python.org/pypi/pymdgen)
[![PyPI](https://img.shields.io/pypi/pyversions/pymdgen.svg?maxAge=600)](https://pypi.python.org/pypi/pymdgen)
[![Travis CI](https://img.shields.io/travis/20c/pymdgen.svg?maxAge=3600)](https://travis-ci.org/20c/pymdgen)
[![Codecov](https://img.shields.io/codecov/c/github/20c/pymdgen/master.svg?maxAge=3600)](https://codecov.io/github/20c/pymdgen)
[![Requires.io](https://img.shields.io/requires/github/20c/pymdgen.svg?maxAge=3600)](https://requires.io/github/20c/pymdgen/requirements)


# Usage

```
Usage: pymdgen [OPTIONS] [MODULES]...

  inspects given python modules and prints markdown

Options:
  --section-level INTEGER  markdown section level
  --help                   Show this message and exit.
```

# Markdown extension

pymddgen also provides a markdown extension that allows you to
easily insert code and command documentation into your generated
docs.

Simply add the `pymdgen` extension to your python markdown instance

### Generate docs for a python module

```
{pymdgen:path.to.python.module}
```

### Generate output for `ls --help`

```
{pymdgen-cmd:ls --help}
```
