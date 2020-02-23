# github-organization-manager

[![Build Status](https://travis-ci.org/ianchesal/github-organization-manager.svg?branch=master)](https://travis-ci.org/ianchesal/github-organization-manager)

A Python CLI for working with organizations in Github.

## Use

This is best done in a virtualenv. To configure one, do:

    pyenv install 3.8.1
    pyenv virtualenv 3.8.1 gom
    pyenv activate gom

Then build the `gom` command:

    pip install --editable .

Now you can use `gom` like so:

    gom --help

It expects you to supply a Github personal access token via the `GOM_GITHUB_TOKEN` environment variable. You can generate one [here](https://github.com/settings/tokens). For permissions the token needs:

## Development

Tests should always be placed in `tests/` and the file names prefixed with `test_` in order to be found by the test runner. The test runner in use is [pytest](https://docs.pytest.org/). You can run all the tests with:

    python setup.py test

This will take care of installing all the necessary test dependencies before excuting the entirety of the test suite for you.

* `repo` (all)
* `admin:org` (all)
* `admin:org_hook`
* `admin:enterprise` (all)
* `workflow`
