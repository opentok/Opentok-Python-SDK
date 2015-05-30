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

*  [tox](https://testrun.org/tox/): a testing automation tool that can load many Python versions.
   This tool allows the project to test against all the compatible versions of Python by leveraging
   virtualenv and describing the tasks in a metadata file.

## Tasks

### Building

Building isn't necessarily required for a python package, but it is possible. By running the command
`$ python setup.py build`, an installable package will be placed in the `build/` directory.

A more useful command is `$ python setup.py develop` which will make the package importable from any
other script in your environment, and continue to update and you make changes.

### Testing

This project's tests are kicked off by tox. The `tox.ini` file describes the automation. In
a nutshell, it selects a Python version, installs test dependencies stored in
`test_requirements.txt`, and then runs `nosetests`. [Nose](https://nose.readthedocs.org) is the
actual test runner. All of this can be ran using the following command: `$ tox`

### Generating Documentation

**TODO**

### Releasing

In order to create a release, the following should be completed in order.

1. Ensure all tests are passing (`tox`) and that there is enough test coverage.
1. Make sure you are on the `master` branch of the repository, with all changes merged/committed already.
1. Update the version number in the source code (`opentok/version.py`) and the README. See [Versioning](#versioning) for
   information about selecting an appropriate version number.
1. Commit the version number change with the message ("Update to version v.x.x.x"), substituting the new version number.
1. Create a git tag: `git tag -a vx.y.z -m "Release vx.y.z"`
1. Ensure you have permission to update the `opentok` package on PyPI: <https://pypi.python.org/pypi/opentok>.
1. Run `python setup.py sdist upload`, which will build and upload the package to PyPI.
1. Change the version number for future development by adding "a1", then make another commit with the message
   "Beginning development on next version".
1. Push the changes to the main repository (`git push origin master`).
1. Upload the `dist/opentok-x.y.z.tar.gz` file to the
   [Github Releases](https://github.com/opentok/opentok-python-sdk/releases) page with a description and release notes.

## Workflow

### Versioning

The project uses [semantic versioning](http://semver.org/) as a policy for incrementing version numbers. For planned
work that will go into a future version, there should be a Milestone created in the Github Issues named with the version
number (e.g. "v2.2.1").

During development the version number should end in "a1" or "bx", where x is an increasing number starting
from 1.

### Branches

*  `master` - the main development branch.
*  `feat.foo` - feature branches. these are used for longer running tasks that cannot be accomplished in one commit.
   once merged into master, these branches should be deleted.
*  `vx.x.x` - if development for a future version/milestone has begun while master is working towards a sooner
   release, this is the naming scheme for that branch. once merged into master, these branches should be deleted.

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
