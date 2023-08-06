# Copyright 2012-2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for `postgresfixture.main`."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

__metaclass__ = type
__all__ = []

from base64 import b16encode
from io import StringIO
from os import urandom
import sys

from fixtures import EnvironmentVariableFixture
from postgresfixture import main
from postgresfixture.cluster import (
    PG_VERSION_MAX,
    PG_VERSIONS,
    )
from postgresfixture.clusterfixture import ClusterFixture
from postgresfixture.testing import TestCase
from testtools.matchers import StartsWith


class TestActions(TestCase):

    class Finished(Exception):
        """A marker exception used for breaking out."""

    def get_random_database_name(self):
        return "db%s" % b16encode(urandom(8)).lower().decode("ascii")

    def parse_args(self, *args):
        try:
            return main.argument_parser.parse_args(args)
        except SystemExit as error:
            self.fail("parse_args%r failed with %r" % (args, error))

    def test_run(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)

        database_name = self.get_random_database_name()

        # Instead of sleeping, check the cluster is running, then break out.
        def sleep_patch(time):
            self.assertTrue(cluster.running)
            self.assertIn(database_name, cluster.databases)
            raise self.Finished

        self.patch(main, "sleep", sleep_patch)
        self.assertRaises(
            self.Finished, main.action_run, cluster,
            self.parse_args("run", "--dbname", database_name))

    def test_run_without_database(self):
        # A database is not created if it's not specified in the PGDATABASE
        # environment variable.
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)

        # Erase the PGDATABASE environment variable, if it's set.
        self.useFixture(
            EnvironmentVariableFixture("PGDATABASE", None))

        # Instead of sleeping, check the cluster is running, then break out.
        def sleep_patch(time):
            self.assertTrue(cluster.running)
            self.assertEqual(
                {"template0", "template1", "postgres"},
                cluster.databases)
            raise self.Finished

        self.patch(main, "sleep", sleep_patch)
        self.assertRaises(
            self.Finished, main.action_run, cluster,
            self.parse_args("run"))

    def test_shell(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)

        database_name = self.get_random_database_name()

        def shell_patch(database):
            self.assertEqual(database_name, database)
            raise self.Finished

        self.patch(cluster, "shell", shell_patch)
        self.assertRaises(
            self.Finished, main.action_shell, cluster,
            self.parse_args("shell", "--dbname", database_name))

    def test_status_running(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)
        cluster.start()
        self.patch(sys, "stdout", StringIO())
        code = self.assertRaises(
            SystemExit, main.action_status, cluster,
            self.parse_args("status")).code
        self.assertEqual(0, code)
        self.assertEqual(
            "%s: running\n" % cluster.datadir,
            sys.stdout.getvalue())

    def test_status_not_running(self):
        cluster = ClusterFixture(self.make_dir())
        cluster.create()
        self.patch(sys, "stdout", StringIO())
        code = self.assertRaises(
            SystemExit, main.action_status, cluster,
            self.parse_args("status")).code
        self.assertEqual(1, code)
        self.assertEqual(
            "%s: not running\n" % cluster.datadir,
            sys.stdout.getvalue())

    def test_status_not_created(self):
        cluster = ClusterFixture(self.make_dir())
        self.patch(sys, "stdout", StringIO())
        code = self.assertRaises(
            SystemExit, main.action_status, cluster,
            self.parse_args("status")).code
        self.assertEqual(2, code)
        self.assertEqual(
            "%s: not created\n" % cluster.datadir,
            sys.stdout.getvalue())

    def test_stop(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)
        cluster.start()
        main.action_stop(cluster, self.parse_args("stop"))
        self.assertFalse(cluster.running)
        self.assertTrue(cluster.exists)

    def test_stop_when_share_locked(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)
        cluster.start()
        self.addCleanup(cluster.shares.release)
        cluster.shares.acquire()
        self.patch(sys, "stderr", StringIO())
        error = self.assertRaises(
            SystemExit, main.action_stop, cluster,
            self.parse_args("stop"))
        self.assertEqual(2, error.code)
        self.assertThat(
            sys.stderr.getvalue(), StartsWith(
                "%s: cluster is locked by:" % cluster.datadir))
        self.assertTrue(cluster.running)

    def test_destroy(self):
        cluster = ClusterFixture(self.make_dir())
        self.addCleanup(cluster.stop)
        cluster.start()
        main.action_destroy(cluster, self.parse_args("destroy"))
        self.assertFalse(cluster.running)
        self.assertFalse(cluster.exists)

    def test_destroy_when_share_locked(self):
        cluster = ClusterFixture(self.make_dir())
        cluster.create()
        cluster.shares.acquire()
        self.patch(sys, "stderr", StringIO())
        error = self.assertRaises(
            SystemExit, main.action_destroy, cluster,
            self.parse_args("destroy"))
        self.assertEqual(2, error.code)
        self.assertThat(
            sys.stderr.getvalue(), StartsWith(
                "%s: cluster is locked by:" % cluster.datadir))
        self.assertTrue(cluster.exists)


class TestVersion(TestCase):

    def patch_pg_versions(self, versions):
        PG_VERSIONS[:] = versions

    def test_uses_supplied_version(self):
        # Reset PG_VERSIONS after the test has run.
        self.addCleanup(self.patch_pg_versions, list(PG_VERSIONS))
        self.patch_pg_versions(["1.1", "2.2", "3.3"])

        # Record calls to our patched handler.
        handler_calls = []

        def handler(cluster, args):
            handler_calls.append((cluster, args))

        self.patch(
            main.get_action("status"), "_defaults",
            {"handler": handler})

        # Prevent main() from altering terminal settings.
        self.patch(main, "setup", lambda: None)

        # The version chosen is picked up by the argument parser and
        # passed into the Cluster constructor.
        main.main(["--version", "2.2", "status"])
        self.assertEqual(
            [("2.2", "2.2")],
            [(cluster.version, args.version)
             for (cluster, args) in handler_calls])

    def test_uses_default_version(self):
        # Record calls to our patched handler.
        handler_calls = []

        def handler(cluster, args):
            handler_calls.append((cluster, args))

        self.patch(
            main.get_action("status"), "_defaults",
            {"handler": handler})

        # The argument parser has the default version and passes it into
        # the Cluster constructor.
        main.main(["status"])
        self.assertEqual(
            [(PG_VERSION_MAX, PG_VERSION_MAX)],
            [(cluster.version, args.version)
             for (cluster, args) in handler_calls])
