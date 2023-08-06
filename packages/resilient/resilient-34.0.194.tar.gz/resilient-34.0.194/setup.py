#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright IBM Corp. 2010, 2017. All Rights Reserved.

""" Setup for resilient module """

from __future__ import print_function
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pkg_resources import get_distribution, DistributionNotFound

try:
    # pip version 10 onward
    from pip._internal.utils.misc import get_installed_distributions
except ImportError:
    from pip import get_installed_distributions


def check_deps():
    # Fail if the 'co3' module is installed, this supersedes it
    packages = get_installed_distributions(local_only=True)
    # For each EggInfoDistribution, find its metadata
    for pkg in packages:
        try:
            distro = get_distribution(pkg.project_name)
            if distro.project_name == 'co3':
                print("This package replaces the 'co3' distribution.  Please 'pip uninstall co3' first.")
                sys.exit(1)
        except DistributionNotFound:
            pass


if __name__ == "__main__":
    check_deps()


class PyTest(TestCommand):
    user_options = [('configfile=', 'c', "Resilient Config File for co3argparse"),
                    ('co3args=', 'a', "Resilient Optional Args for co3argparse"),
                    ('pytestargs=', 'p', "Pytest Optional Args")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.configfile = ""
        self.co3args = ""
        self.pytestargs = ""
        self.test_suite = True
        self.test_args = []

    def finalize_options(self):
        import shlex
        TestCommand.finalize_options(self)
        if self.configfile:
            self.test_args += ["--config-file=%s" % self.configfile]
        if self.co3args:
            self.test_args += ["--co3args=%s" % self.co3args]
        if self.pytestargs:
            self.test_args += shlex.split(self.pytestargs)

    def run_tests(self):
        # import here, because outside the eggs aren't loaded
        print("Running Tests with args: %s" % self.test_args)
        import pytest
        errno = pytest.main(args=self.test_args)
        sys.exit(errno)


setup(
    name='resilient',
    use_scm_version={"root": "../", "relative_to": __file__},
    setup_requires=['setuptools_scm'],
    url='https://developer.ibm.com/resilient',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    author='IBM Resilient',
    install_requires=[
        'argparse',
        'requests>=2.6.0',
        'requests-toolbelt>=0.6.0',
        'requests-mock>=1.2.0',
        'six',
        'cachetools<3.0.0'
    ],
    extras_require={
        ':python_version < "3.2"': [
            'configparser'
        ],
        ':python_version >= "3.5"': [
            'keyring'
        ],
        ':python_version < "3.5"': [
            'keyring>=5.4,<19.0.0'
        ]
    },
    tests_require=["pytest>=3.0.0, <4.1.0", ],
    cmdclass={"test": PyTest},
    author_email='support@resilientsystems.com',
    description='Resilient API',
    long_description='Resilient API Modules for Python',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': ['finfo = resilient.bin.finfo:main',
                            'gadget = resilient.bin.gadget:main',
                            'res-keyring = resilient.bin.res_keyring:main']
    }
)
