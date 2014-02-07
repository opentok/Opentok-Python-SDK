from os.path import abspath, dirname, join, normpath

from setuptools import setup
import OpenTokSDK


setup(

    # Basic package information:
    name = 'opentok-python-sdk',
    version = OpenTokSDK.__version__,
    py_modules = ['OpenTokSDK'],
    install_requires=['requests == 1.2.3'],

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Metadata for PyPI:
    author = 'TokBox, Inc.',
    author_email = 'support@tokbox.com',
    #license = '?',
    url = 'https://github.com/opentok/Opentok-Python-SDK',
    keywords = 'video chat tokbox tok opentok python media',
    description = 'A python wrapper for the OpenTok video chat APIs.',
    long_description = open(normpath(join(dirname(abspath(__file__)),
        'README.md'))).read(),
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
