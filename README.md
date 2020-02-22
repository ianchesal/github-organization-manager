# github-organization-manager

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

* `repo` (all)
* `admin:org` (all)
* `admin:org_hook`
* `admin:enterprise` (all)
* `workflow`
