# Copyright 2012-2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Testing resources for `postgresfixture`."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

__metaclass__ = type
__all__ = [
    "TestCase",
    ]

from fixtures import TempDir
import testtools


class TestCase(testtools.TestCase):
    """Convenience subclass."""

    def make_dir(self):
        return self.useFixture(TempDir()).path
