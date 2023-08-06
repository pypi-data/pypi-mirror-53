# Copyright 2012-2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for `postgresfixture.clusterfixture`."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

__metaclass__ = type
__all__ = []

from os import (
    getpid,
    path,
    )

from postgresfixture.clusterfixture import (
    ClusterFixture,
    ProcessSemaphore,
    )
from postgresfixture.testing import TestCase
from postgresfixture.tests import test_cluster
from testtools.matchers import (
    FileExists,
    Not,
    )


class TestProcessSemaphore(TestCase):

    def test_init(self):
        lockdir = self.make_dir()
        psem = ProcessSemaphore(lockdir)
        self.assertEqual(lockdir, psem.lockdir)
        self.assertEqual(
            path.join(lockdir, "%s" % getpid()),
            psem.lockfile)

    def test_acquire(self):
        psem = ProcessSemaphore(
            path.join(self.make_dir(), "locks"))
        psem.acquire()
        self.assertThat(psem.lockfile, FileExists())
        self.assertTrue(psem.locked)
        self.assertEqual([getpid()], psem.locked_by)

    def test_release(self):
        psem = ProcessSemaphore(
            path.join(self.make_dir(), "locks"))
        psem.acquire()
        psem.release()
        self.assertThat(psem.lockfile, Not(FileExists()))
        self.assertFalse(psem.locked)
        self.assertEqual([], psem.locked_by)


class TestClusterFixture(test_cluster.TestCluster):

    def make(self, *args, **kwargs):
        kwargs.setdefault("version", self.version)
        fixture = ClusterFixture(*args, **kwargs)
        # Run the basic fixture set-up so that clean-ups can be added.
        super(ClusterFixture, fixture).setUp()
        return fixture

    def test_init_fixture(self):
        fixture = self.make("/some/where")
        self.assertEqual(False, fixture.preserve)
        self.assertIsInstance(fixture.shares, ProcessSemaphore)
        self.assertEqual(
            path.join(fixture.datadir, "shares"),
            fixture.shares.lockdir)

    def test_createdb_no_preserve(self):
        fixture = self.make(self.make_dir(), preserve=False)
        self.addCleanup(fixture.stop)
        fixture.start()
        fixture.createdb("danzig")
        self.assertIn("danzig", fixture.databases)
        # The database is only created if it does not already exist.
        fixture.createdb("danzig")
        # Creating a database arranges for it to be dropped when stopping the
        # fixture.
        fixture.cleanUp()
        self.assertNotIn("danzig", fixture.databases)

    def test_createdb_preserve(self):
        fixture = self.make(self.make_dir(), preserve=True)
        self.addCleanup(fixture.stop)
        fixture.start()
        fixture.createdb("emperor")
        self.assertIn("emperor", fixture.databases)
        # The database is only created if it does not already exist.
        fixture.createdb("emperor")
        # Creating a database arranges for it to be dropped when stopping the
        # fixture.
        fixture.cleanUp()
        self.assertIn("emperor", fixture.databases)

    def test_dropdb(self):
        fixture = self.make(self.make_dir())
        self.addCleanup(fixture.stop)
        fixture.start()
        # The database is only dropped if it exists.
        fixture.dropdb("diekrupps")
        fixture.dropdb("diekrupps")
        # The test is that we arrive here without error.

    def test_stop_share_locked(self):
        # The cluster is not stopped if a shared lock is held.
        fixture = self.make(self.make_dir())
        self.addCleanup(fixture.stop)
        fixture.start()
        fixture.shares.acquire()
        fixture.stop()
        self.assertTrue(fixture.running)
        fixture.shares.release()
        fixture.stop()
        self.assertFalse(fixture.running)

    def test_destroy_share_locked(self):
        # The cluster is not destroyed if a shared lock is held.
        fixture = self.make(self.make_dir())
        fixture.create()
        fixture.shares.acquire()
        fixture.destroy()
        self.assertTrue(fixture.exists)
        fixture.shares.release()
        fixture.destroy()
        self.assertFalse(fixture.exists)

    def test_use_no_preserve(self):
        # The cluster is stopped and destroyed when preserve=False.
        with self.make(self.make_dir(), preserve=False) as fixture:
            self.assertTrue(fixture.exists)
            self.assertTrue(fixture.running)
        self.assertFalse(fixture.exists)
        self.assertFalse(fixture.running)

    def test_use_no_preserve_cluster_already_exists(self):
        # The cluster is stopped but *not* destroyed when preserve=False if it
        # existed before the fixture was put into use.
        fixture = self.make(self.make_dir(), preserve=False)
        fixture.create()
        with fixture:
            self.assertTrue(fixture.exists)
            self.assertTrue(fixture.running)
        self.assertTrue(fixture.exists)
        self.assertFalse(fixture.running)

    def test_use_preserve(self):
        # The cluster is not stopped and destroyed when preserve=True.
        with self.make(self.make_dir(), preserve=True) as fixture:
            self.assertTrue(fixture.exists)
            self.assertTrue(fixture.running)
            fixture.createdb("gallhammer")
        self.assertTrue(fixture.exists)
        self.assertFalse(fixture.running)
        self.addCleanup(fixture.stop)
        fixture.start()
        self.assertIn("gallhammer", fixture.databases)

    def test_namespace(self):
        # ClusterFixture is in the postgresfixture namespace.
        import postgresfixture
        self.assertIs(postgresfixture.ClusterFixture, ClusterFixture)
