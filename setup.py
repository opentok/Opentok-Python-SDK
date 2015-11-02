from setuptools import setup, find_packages
import codecs
import os
import re
import sys

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'requests',
    'six',
    'pytz',
]

if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    install_requires.append('enum34')

setup(
    name = 'opentok',
    version = find_version('opentok', 'version.py'),
    description = 'OpenTok server-side SDK',
    long_description=long_description,

    url = 'https://github.com/opentok/Opentok-Python-SDK',

    author='TokBox, Inc.',
    author_email='support@tokbox.com',
    license='LICENSE.txt',

    classifiers = [
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    keywords = 'video chat tokbox tok opentok python media webrtc archiving realtime',

    packages=find_packages(exclude=["contrib", "docs", "tests*"]),

    install_requires=install_requires,

    include_package_data = True,
)
