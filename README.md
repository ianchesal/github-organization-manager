# github-organization-manager

[![Build Status](https://travis-ci.org/ianchesal/github-organization-manager.svg?branch=master)](https://travis-ci.org/ianchesal/github-organization-manager)

A Python CLI for working with organizations in Github.

## Use

This is best done in a pipenv-managed virtualenv. To configure one, do:

    brew install pipenv pyenv
    pipenv --python 3.8
    pipenv install '-e .'
    pipenv shell

Now you can use `gom` like so:

    gom --help

It expects you to supply a Github personal access token via the `GOM_GITHUB_TOKEN` environment variable. You can generate one [here](https://github.com/settings/tokens). For permissions the token needs:

## Development

Tests should always be placed in `tests/` and the file names prefixed with `test_` in order to be found by the test runner. The test runner in use is [pytest](https://docs.pytest.org/). You can run all the tests with:

    python setup.py test

This will take care of installing all the necessary test dependencies before excuting the entirety of the test suite for you.

If you rely on new packages remember to add them to `setup.py` so they're installed as dependencies for everyone else. The list of packages should be minimal. After you add a package to `setup.py` you'll need to regenerate the `Pipfile.lock` file by running `pipenv install '-e .'`. This ensures anyone else gets the packages at the same version as you when they go to work with the code.

* `repo` (all)
* `admin:org` (all)
* `admin:org_hook`
* `admin:enterprise` (all)
* `workflow`
