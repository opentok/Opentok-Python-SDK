# Development Guidelines

This document describes tools, tasks and workflow that one needs to be familiar with in order to effectively maintain
this project. If you use this package within your own software as is but don't plan on modifying it, this guide is
**not** for you.

## Tools

*  [Pip](https://pip.pypa.io/): a command line package installer for Python. This tool is typically
   included with recent versions of Python.

*  [virtualenv](https://virtualenv.pypa.io/): a tool to create isolated Python environments. The
   first thing you should do once you've cloned this repository is to run `pip install virtualenv;
   virtualenv venv; source venv/bin/activate` to create an environment and load it in your shell.
   This helps keep all the python packages you install and use isolated into a project specific
   location on your system, which helps keep you out of dependency hell. You can exit the
   environment using `$ deactivate`.

*  [act](https://github.com/nektos/act): a tool for running Github Actions locally. This tool allows
   developers to easily replicate the same Continuous Integration pipelines we use for code validation.

## Tasks

## Setup

We currently recommend setting up a development environment using `virtualenv` and installing dependencies
with `pip`. While the Python Packaging Authority recommends `Pipenv` to manage dependencies, `Pipenv` does
not install the OpenTok library correctly from source at this time.

We recommend setting up a Python 3.5 or higher `virtualenv` environment. This allows you to isolate dependencies
for work on the OpenTok library without interfering with any other projects or installations on your system.

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt -r test_requirements.txt

Some IDEs, like Visual Studio Code, will automatically detect the `virtualenv` and use it. 

When you are done, you can leave the `virtualenv` by deactivating it:

    $ deactivate

### Building

Building isn't necessarily required for a python package, but it is possible. By running the command
`$ python setup.py build`, an installable package will be placed in the `build/` directory.

A more useful command is `$ python setup.py develop` which will make the package importable from any
other script in your environment, and continue to update and you make changes.

### Testing

This project's tests are built using the `unittest` [Pytest](https://docs.pytest.org/en/stable/) modules.
To run the unit tests, install the core as well as development dependencies inside your `virtualenv`:

    $ pip install -r requirements.txt -r test_requirements.txt

You can manually run the test suite for your version of python with:

    $ pytest

If you would like to run the test suite against a variety of Python versions, we recommend installing
`act` and running out Github Action "test" workflow:

    $ act --quiet

### Generating Documentation

**TODO**

### Releasing

In order to create a release, the following should be completed in order.

#### Prep the release

1. Ensure all tests are passing (`act`) and that there is enough test coverage.
1. Make sure you are on the `master` branch of the repository, with all changes merged/committed already.
1. Create a new branch named `release-x.y.z`, with the release version number
1. Update the version number with `bumpversion`. See [Versioning](#versioning) for
   information about selecting an appropriate version number.
1. Commit the version number change with the message ("Update to version v.x.x.x"), substituting the new version number.
1. Create a new pull request with this branch

#### Once PR is merged into `master`
1. Make sure you are on the `master` branch of the repository
1. Run `git pull --rebase origin master` to make sure your local code is up-to-date
1. Create a git tag: `git tag -a vx.y.z -m "Release vx.y.z"`
1. Run `git push origin vx.y.z` to push the tag to Github
1. Ensure you have permission to update the `opentok` package on PyPI: <https://pypi.python.org/pypi/opentok>.
1. Run the deploy scripts:
  1. `make clean`
  1. `make dist`
  1. `make release`
1. Create a new release on the [Github Releases](https://github.com/opentok/opentok-python-sdk/releases) page,
   and attach the files in `dist/` to the release

## Workflow

### Versioning

The project uses [semantic versioning](http://semver.org/) as a policy for incrementing version numbers. For planned
work that will go into a future version, there should be a Milestone created in the Github Issues named with the version
number (e.g. "v2.2.1").

During development the version number should end in "a1" or "bx", where x is an increasing number starting
from 1.

### Branches

*  `master` - the main development branch.

### Tags

*  `vx.x.x` - commits are tagged with a final version number during release.

### Issues

Issues are labelled to help track their progress within the pipeline.

*  no label - these issues have not been triaged.
*  `bug` - confirmed bug. aim to have a test case that reproduces the defect.
*  `enhancement` - contains details/discussion of a new feature. it may not yet be approved or placed into a
   release/milestone.
*  `wontfix` - closed issues that were never addressed.
*  `duplicate` - closed issue that is the same to another referenced issue.
*  `question` - purely for discussion

### Management

When in doubt, find the maintainers and ask.
