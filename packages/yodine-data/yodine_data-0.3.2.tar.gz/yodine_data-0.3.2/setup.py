from setuptools import setup
from yodine_data.version import VERSION_STR as VERSION

import os



NAME = 'yodine_data'
DESCRIPTION = 'All the assets, entities and levels that come with Yodine (the game). Note there can be multiple games for Yodine (the engine).'
AUTHOR = 'Gustavo6046'
REQUIRES_PYTHON = '>=3.5.0'
LICENSE = 'MIT'


# What packages are required for this plugin to work?
REQUIRED = [
    # Yodine plugin dependencies:
    'yodine_data',

    # General dependencies:
    # 'numpy'
]

with open('README.md') as readme:
    long_description = readme.read()
        

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    packages=['yodine_data'],

    entry_points={
        'yodine.plugin': ['{0} = {0}.plugin:loaded'.format(NAME)],
    },
    install_requires=REQUIRED,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    package_data={NAME: ['assets/*', 'assets/**/*']},
    include_package_data=True,
)
