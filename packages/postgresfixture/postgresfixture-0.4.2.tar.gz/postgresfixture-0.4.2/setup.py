#!/usr/bin/env python
# Copyright 2012-2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Distutils installer for postgresfixture."""

from __future__ import (
    absolute_import,
    print_function,
    )

__metaclass__ = type

import codecs

from setuptools import (
    find_packages,
    setup,
    )


with codecs.open("requirements.txt", "rb", encoding="utf-8") as fd:
    requirements = [line.strip() for line in fd]


with open("README.txt") as readme:
    long_description = readme.read()


setup(
    name='postgresfixture',
    version="0.4.2",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=("testtools >= 0.9.14",),
    test_suite="postgresfixture.tests",
    include_package_data=True,
    zip_safe=False,
    description=(
        "A fixture for creating PostgreSQL clusters and databases, and "
        "tearing them down again, intended for use during development "
        "and testing."),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    entry_points={
        "console_scripts": [
            "postgresfixture = postgresfixture.main:main",
            ],
        },
    )
