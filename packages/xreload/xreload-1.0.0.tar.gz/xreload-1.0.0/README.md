[![pypi\_version\_img](https://img.shields.io/pypi/v/xreload.svg?style=flat)](https://pypi.python.org/pypi/xreload) [![Supported Python versions](https://img.shields.io/pypi/pyversions/xreload.svg)](https://pypi.python.org/pypi/xreload) [![pypi\_license\_img](https://img.shields.io/pypi/l/xreload.svg?style=flat)](https://pypi.python.org/pypi/xreload) [![travis\_build\_status](https://travis-ci.org/Lucas-C/xreload.svg?branch=master)](https://travis-ci.org/Lucas-C/xreload)

# xreload

This is Pypi-packaged version of Guido van Rossum original `xreload.py` script:
<http://svn.python.org/projects/sandbox/trunk/xreload/>

It also re-use some changes to this code made on the `plone.reload` package:
<https://github.com/plone/plone.reload/blob/master/plone/reload/xreload.py>

## License

Neither Guido's original code nor `plone.reload` code has any specific license,
so none is provided with this package.

## Usage

    from xreload import xreload
    xreload(sys.modules[__name__], new_annotations={'RELOADING': True})

## Development
### Releasing a new version
With a valid `~/.pypirc`:

1. edit version in `setup.py`
2. `python setup.py sdist`
3. `twine upload dist/*`
4. `git tag $version && git push && git push --tags`
