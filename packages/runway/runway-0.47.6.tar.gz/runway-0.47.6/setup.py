"""Packaging settings."""

from codecs import open as codecs_open
from os.path import abspath, dirname, join
from sys import version_info

from setuptools import find_packages, setup

from runway import __version__


THIS_DIR = abspath(dirname(__file__))
with codecs_open(join(THIS_DIR, 'README.rst'), encoding='utf-8') as readfile:
    LONG_DESCRIPTION = readfile.read()


INSTALL_REQUIRES = [
    'Send2Trash',
    'awacs',  # for embedded hooks
    'awscli>=1.16.121<2.0'  # for embedded hooks; matching stacker requirement
    'botocore>=1.12.111',  # matching awscli/boto3 requirement
    'boto3>=1.9.111<2.0'  # matching stacker requirement
    'PyYAML~=3.13',  # matching awscli requirement
    'cfn_flip<=1.2.0',  # 1.2.1+ require PyYAML 4.1+
    'cfn-lint',
    'docopt',
    'flake8',
    'flake8-docstrings',
    'pep8-naming',
    'future',
    # embedded pyhcl is 0.3.12
    # with the LICENSE file added to its root folder
    # and the following patches applied
    # https://github.com/virtuald/pyhcl/pull/57
    'pyhcl~=0.3',
    'six',
    'typing',
    'yamllint',
    'zgitignore',  # for embedded hooks
    # embedded stacker is v1.7.0
    # with the LICENSE file added to its root folder
    # and the following patches applied
    # https://github.com/cloudtools/stacker/pull/731 (CAPABILITY_AUTO_EXPAND)
    # and the following files/folders deleted:
    #   * tests
    #   * blueprints/testutil.py
    # and the stacker & stacker.cmd scripts adapted with EMBEDDED_LIB_PATH
    'stacker~=1.7',
    # stacker's troposphere dep is more loose, but we need to ensure we use a
    # sufficiently recent version for compatibility embedded blueprints
    'troposphere>=2.4.2',
    # botocore pins its urllib3 dependency like this, so we need to do the
    # same to ensure v1.25+ isn't pulled in by pip
    'urllib3>=1.20,<1.25',
    # python3 flake8-docstrings fails with pydocstyle 4:
    # https://github.com/PyCQA/pydocstyle/issues/375
    # newer versions do not support python2:
    # https://github.com/PyCQA/pydocstyle/pull/374
    "pydocstyle<=3.0.0"
]

# pylint v2+ is only py3 compatible
if version_info[0] == 2:
    INSTALL_REQUIRES.append('pylint~=1.9')
else:
    INSTALL_REQUIRES.append('pylint')

setup(
    name='runway',
    version=__version__,
    description='Simplify infrastructure/app testing/deployment',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/onicagroup/runway',
    author='Onica Group LLC',
    author_email='opensource@onica.com',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=2.6',
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'test': ['flake8', 'pep8-naming', 'flake8-docstrings', 'pylint'],
    },
    entry_points={
        'console_scripts': [
            'runway=runway.cli:main',
        ],
    },
    scripts=['scripts/stacker-runway', 'scripts/stacker-runway.cmd',
             'scripts/tf-runway', 'scripts/tf-runway.cmd',
             'scripts/tfenv-runway', 'scripts/tfenv-runway.cmd'],
    include_package_data=True,  # needed for templates,blueprints,hooks
    test_suite='tests'
)
