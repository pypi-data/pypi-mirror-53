# Copyright 2012-2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for `postgresfixture.cluster`."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

__metaclass__ = type
__all__ = []

from contextlib import closing
import io
from os import (
    getpid,
    path,
    )
import subprocess
from subprocess import (
    CalledProcessError,
    PIPE,
    Popen,
    )
import sys
from textwrap import dedent

import postgresfixture.cluster
from postgresfixture.cluster import (
    Cluster,
    get_pg_bin,
    path_with_pg_bin,
    PG_VERSIONS,
    )
from postgresfixture.main import repr_pid
from postgresfixture.testing import TestCase
from postgresfixture.utils import LockAlreadyTaken
from testscenarios import WithScenarios
from testtools import ExpectedException
from testtools.content import text_content
from testtools.matchers import (
    DirExists,
    FileExists,
    Not,
    StartsWith,
    )


class TestFunctions(WithScenarios, TestCase):

    scenarios = sorted(
        (version, {"version": version})
        for version in PG_VERSIONS
    )

    def test_path_with_pg_bin(self):
        pg_bin = get_pg_bin(self.version)
        self.assertEqual(pg_bin, path_with_pg_bin("", self.version))
        self.assertEqual(
            pg_bin + path.pathsep + "/bin:/usr/bin",
            path_with_pg_bin("/bin:/usr/bin", self.version))

    def test_repr_pid_not_a_number(self):
        self.assertEqual("alice", repr_pid("alice"))
        self.assertEqual("'alice and bob'", repr_pid("alice and bob"))

    def test_repr_pid_not_a_process(self):
        self.assertEqual("0 (*unknown*)", repr_pid(0))

    def test_repr_pid_this_process(self):
        pid = getpid()
        self.assertThat(repr_pid(pid), StartsWith("%d (" % pid))


class TestCluster(WithScenarios, TestCase):

    scenarios = sorted(
        (version, {"version": version})
        for version in PG_VERSIONS
    )

    def make(self, *args, **kwargs):
        kwargs.setdefault("version", self.version)
        return Cluster(*args, **kwargs)

    def test_init(self):
        # The datadir passed into the Cluster constructor is resolved to an
        # absolute path.
        tmpdir = self.make_dir()
        datadir = path.join(tmpdir, "somewhere")
        cluster = self.make(path.relpath(datadir))
        self.assertEqual(datadir, cluster.datadir)
        # The lock file is in the parent directory of the data directory.
        self.assertEqual(
            path.join(tmpdir, ".somewhere.lock"),
            cluster.lock.path)

    def test_lock(self):
        # To test the lock - based on lockf - we take the lock locally then
        # check if it appears locked from a separate process.
        cluster = self.make(self.make_dir())
        script = dedent("""\
            from errno import EAGAIN
            from fcntl import LOCK_EX, LOCK_NB, lockf
            with open(%r, "ab") as fd:
                try:
                    lockf(fd, LOCK_EX | LOCK_NB)
                except IOError as error:
                    if error.errno != EAGAIN:
                        raise
                else:
                    raise AssertionError("Not locked")
            """) % cluster.lock.path
        with cluster.lock.exclusive:
            process = Popen(
                sys.executable, stdin=PIPE,
                stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate(script.encode("ascii"))
            self.addDetail("stdout", text_content(stdout.decode("ascii")))
            self.addDetail("stderr", text_content(stderr.decode("ascii")))
            self.assertEqual(0, process.returncode)

    def test_exclusive_lock_is_not_reentrant(self):
        # The lock cannot be acquired more than once.
        cluster = self.make(self.make_dir())
        with cluster.lock.exclusive:
            with ExpectedException(LockAlreadyTaken):
                with cluster.lock.exclusive:
                    pass  # We won't get here.

    def test_shared_lock_is_not_reentrant(self):
        # The lock cannot be acquired more than once.
        cluster = self.make(self.make_dir())
        with cluster.lock.shared:
            with ExpectedException(LockAlreadyTaken):
                with cluster.lock.shared:
                    pass  # We won't get here.

    def patch_check_call(self, returncode=0):
        calls = []

        def check_call(command, **options):
            calls.append((command, options))
            if returncode != 0:
                raise CalledProcessError(returncode, command)

        self.patch(postgresfixture.cluster, "check_call", check_call)
        return calls

    def test_execute(self):
        calls = self.patch_check_call()
        cluster = self.make(self.make_dir())
        cluster.execute("true")
        [(command, options)] = calls
        self.assertEqual(("true",), command)
        self.assertIn("env", options)
        env = options["env"]
        self.assertEqual(cluster.datadir, env.get("PGDATA"))
        self.assertEqual(cluster.datadir, env.get("PGHOST"))
        self.assertThat(
            env.get("PATH", ""),
            StartsWith(get_pg_bin(self.version) + path.pathsep))

    def test_exists(self):
        cluster = self.make(self.make_dir())
        # The PG_VERSION file is used as a marker of existence.
        version_file = path.join(cluster.datadir, "PG_VERSION")
        self.assertThat(version_file, Not(FileExists()))
        self.assertFalse(cluster.exists)
        open(version_file, "wb").close()
        self.assertTrue(cluster.exists)

    def test_pidfile(self):
        self.assertEqual(
            "/some/where/postmaster.pid",
            self.make("/some/where").pidfile)

    def test_logfile(self):
        self.assertEqual(
            "/some/where/backend.log",
            self.make("/some/where").logfile)

    def test_running_calls_pg_ctl(self):
        calls = self.patch_check_call(returncode=0)
        cluster = self.make(self.make_dir())
        self.assertTrue(cluster.running)
        [(command, options)] = calls
        self.assertEqual(("pg_ctl", "status"), command)

    def test_running(self):
        cluster = self.make(self.make_dir())
        cluster.start()
        self.assertTrue(cluster.running)

    def test_running_not(self):
        cluster = self.make(self.make_dir())
        self.assertFalse(cluster.running)

    def test_running_error(self):
        self.patch_check_call(returncode=2)  # Unrecognised code.
        cluster = self.make(self.make_dir())
        self.assertRaises(
            CalledProcessError, getattr, cluster, "running")

    def test_running_captures_stderr(self):
        # stderr is captured when running pg_ctl and not normally printed.
        def check_call(command, **options):
            return subprocess.check_call(
                ('/bin/sh', '-c', 'echo foobar >&2 && exit 0'), **options)
        self.patch(postgresfixture.cluster, "check_call", check_call)
        self.patch(sys, "stderr", io.BytesIO())
        cluster = self.make(self.make_dir())
        self.assertTrue(cluster.running)
        self.assertEqual(b"", sys.stderr.getvalue())

    def test_running_captures_and_replays_stderr_on_error(self):
        # stderr is captured when running pg_ctl and replayed on error.
        def check_call(command, **options):
            return subprocess.check_call(
                ('/bin/sh', '-c', 'echo foobar >&2 && exit 2'), **options)
        self.patch(postgresfixture.cluster, "check_call", check_call)
        self.patch(sys, "stderr", io.BytesIO())
        cluster = self.make(self.make_dir())
        self.assertRaises(CalledProcessError, getattr, cluster, "running")
        self.assertEqual(b"foobar\n", sys.stderr.getvalue())

    def test_create(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        self.assertTrue(cluster.exists)
        self.assertFalse(cluster.running)

    def test_start_and_stop(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        try:
            cluster.start()
            self.assertTrue(cluster.running)
        finally:
            cluster.stop()
            self.assertFalse(cluster.running)

    def test_connect(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        self.addCleanup(cluster.stop)
        cluster.start()
        with closing(cluster.connect()) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute("SELECT 1")
                self.assertEqual([(1,)], cur.fetchall())

    def test_databases(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        self.addCleanup(cluster.stop)
        cluster.start()
        self.assertEqual(
            {"postgres", "template0", "template1"},
            cluster.databases)

    def test_createdb_and_dropdb(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        self.addCleanup(cluster.stop)
        cluster.start()
        cluster.createdb("setherial")
        self.assertEqual(
            {"postgres", "template0", "template1", "setherial"},
            cluster.databases)
        cluster.dropdb("setherial")
        self.assertEqual(
            {"postgres", "template0", "template1"},
            cluster.databases)

    def test_destroy(self):
        cluster = self.make(self.make_dir())
        cluster.create()
        cluster.destroy()
        self.assertFalse(cluster.exists)
        self.assertFalse(cluster.running)
        self.assertThat(cluster.datadir, Not(DirExists()))
