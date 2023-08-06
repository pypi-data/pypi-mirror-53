#
# Copyright 2019 Ricardo Branco <rbranco@suse.de>
# MIT License
#
"""
Module with classes to parse /proc entries
"""

import gzip
import os
import re
from itertools import zip_longest

from restartable.attrdict import AttrDict, FSDict


class _Mixin:
    """
    Mixin class to share methods between Proc() and ProcPid()
    """

    _dir_fd = None

    def __del__(self):
        if self._dir_fd is not None:
            os.close(self._dir_fd)
        self._dir_fd = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._dir_fd is not None:
            os.close(self._dir_fd)
        self._dir_fd = None

    def _get_dirfd(self, path, dir_fd=None):
        """
        Get directory file descriptor
        """
        self._dir_fd = os.open(path, os.O_RDONLY, dir_fd=dir_fd)


class Property:  # pylint: disable=too-few-public-methods
    """
    Simple property class decorator to avoid boilerplate code
    """
    def __init__(self, fget=None):
        self.fget = fget
        self.name = fget.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.name not in obj:
            obj[self.name] = self.fget(obj)
        return obj[self.name]


class Proc(FSDict, _Mixin):  # pylint: disable=too-many-ancestors
    """
    Class to parse /proc entries
    """
    def __init__(self, proc="/proc"):
        self._proc = proc
        self._get_dirfd(proc)
        super().__init__()

    def __repr__(self):
        return "%s(proc=%s)" % (type(self).__name__, self._proc)

    def pids(self):
        """
        Returns a list of all the processes in the system
        """
        return filter(str.isdigit, os.listdir(self._dir_fd))

    def tasks(self):
        """
        Returns a list of all the tasks (threads) in the system
        """
        #  We could use a list comprehension but a PID could disappear
        for pid in self.pids():
            with ProcPid(pid, dir_fd=self._dir_fd) as proc:
                try:
                    yield from proc.task
                except FileNotFoundError:
                    pass

    @Property
    def config(self):
        """
        Parses /proc/config.gz and returns an AttrDict
        If /proc/config.gz doesn't exist, try /boot or /lib/modules/
        """
        lines = None
        paths = [
            "config.gz",
            "/boot/config-%s" % os.uname().release,
            "/lib/modules/%s/build/.config" % os.uname().release
        ]
        for path in paths:
            try:
                os.stat(path, dir_fd=self._dir_fd)
            except FileNotFoundError:
                continue
            if path.endswith(".gz"):
                with open(path, "rb", opener=self._opener) as f:
                    with gzip.open(f) as file:
                        lines = file.read().decode('utf-8').splitlines()
            else:
                with open(path) as file:
                    lines = file.read().splitlines()
            break
        if lines is None:
            return None
        return AttrDict(
            line.split('=') for line in lines if line.startswith("CONFIG_"))

    @Property
    def cgroups(self):
        """
        Parses /proc/cgroup and returns a list of AttrDict's
        """
        with open("cgroups", opener=self._opener) as file:
            data = file.read()
        keys, *values = data.splitlines()
        return [AttrDict(zip(keys[1:].split(), _.split())) for _ in values]

    @Property
    def cmdline(self):
        """
        Parses /proc/cmdline and returns a list
        """
        with open("cmdline", opener=self._opener) as file:
            return file.read().strip()

    @Property
    def cpuinfo(self):
        """
        Parses /proc/cpuinfo and returns a list of AttrDict's
        """
        with open("cpuinfo", opener=self._opener) as file:
            cpus = [file.read()[:-1].split('\n\n')]
        return [
            AttrDict([map(str.strip, line.split(':'))
                      for line in cpu.splitlines()])
            for cpu in cpus]

    @Property
    def meminfo(self):
        """
        Parses /proc/meminfo and returns an AttrDict
        """
        with open("meminfo", opener=self._opener) as file:
            lines = file.read().splitlines()
        return AttrDict([map(str.strip, line.split(':')) for line in lines])

    @Property
    def mounts(self):
        """
        Parses /proc/mounts and returns a list of AttrDict's
        """
        # /proc/mounts is a symlink to /proc/self/mounts
        with ProcPid(dir_fd=self._dir_fd) as proc_self:
            return proc_self.mounts

    @Property
    def swaps(self):
        """
        Parses /proc/swaps and returns a list of AttrDict's
        """
        with open("swaps", opener=self._opener) as file:
            data = file.read()
        keys, *values = data.splitlines()
        return [AttrDict(zip(keys.split(), _.split())) for _ in values]

    @Property
    def vmstat(self):
        """
        Parses /proc/vmstat and returns an AttrDict
        """
        with open("vmstat", opener=self._opener) as file:
            data = file.read()
        return AttrDict(line.split() for line in data.splitlines())

    def _sysvipc(self, path):
        """
        Parses /proc/sysvipc/{msg,sem,shm} and returns a list of AttrDict's
        """
        with open(os.path.join("sysvipc", path), opener=self._opener) as file:
            data = file.read()
        keys, *values = data.splitlines()
        return [AttrDict(zip(keys.split(), _.split())) for _ in values]

    def __missing__(self, path):
        """
        Creates dynamic attributes for elements in /proc/
        """
        if path in ("config", "cgroups", "cmdline", "cpuinfo",
                    "meminfo", "mounts", "swaps", "vmstat"):
            return getattr(self, path)
        if path == "self":
            return ProcPid(dir_fd=self._dir_fd)
        if path.isdigit():
            return ProcPid(path, dir_fd=self._dir_fd)
        if path == "sysvipc":
            return FSDict(path=path, dir_fd=self._dir_fd, handler=self._sysvipc)
        return super().__missing__(path)


_limits_fields = {
    'Max cpu time': 'cpu',
    'Max file size': 'fsize',
    'Max data size': 'data',
    'Max stack size': 'stack',
    'Max core file size': 'core',
    'Max resident set': 'rss',
    'Max processes': 'nproc',
    'Max open files': 'nofile',
    'Max locked memory': 'memlock',
    'Max address space': 'as',
    'Max file locks': 'locks',
    'Max pending signals': 'sigpending',
    'Max msgqueue size': 'msgqueue',
    'Max nice priority': 'nice',
    'Max realtime priority': 'rtprio',
    'Max realtime timeout': 'rttime',
}

_maps_fields = ('address', 'perms', 'offset', 'dev', 'inode', 'pathname')

_mounts_fields = ('fs_spec', 'fs_file', 'fs_vfstype',
                  'fs_mntops', 'fs_freq', 'fs_passno')

_stat_fields = (
    'pid comm state ppid pgrp session tty_nr tpgid flags '
    'minflt cminflt majflt cmajflt utime stime cutime cstime '
    'priority nice num_threads itrealvalue starttime vsize rss rsslim '
    'startcode endcode startstack kstkesp kstkeip signal blocked '
    'sigignore sigcatch wchan nswap cnswap exit_signal processor '
    'rt_priority policy delayacct_blkio_ticks guest_time cguest_time '
    'start_data end_data start_brk arg_start arg_end env_start env_end '
    'exit_code').split()

_statm_fields = ('size', 'resident', 'shared', 'text', 'lib', 'data', 'dt')

_status_XID_fields = ('real', 'effective', 'saved_set', 'filesystem')


class ProcPid(FSDict, _Mixin):  # pylint: disable=too-many-ancestors
    """
    Class for managing /proc/<pid>/*
    """
    def __init__(self, pid=None, proc="/proc", dir_fd=None):
        if pid is None:
            pid = os.getpid()
        if not isinstance(pid, (int, str)) and int(pid) <= 0:
            raise ValueError("Invalid pid %s" % pid)
        self.pid = str(pid)
        if dir_fd is None:
            self._get_dirfd(os.path.join(proc, self.pid))
        else:
            self._get_dirfd(self.pid, dir_fd=dir_fd)
        self._proc = proc
        super().__init__()

    def __repr__(self):
        return "%s(pid=%s, proc=%s)" % (
            type(self).__name__, self.pid, self._proc)

    @Property
    def cmdline(self):
        """
        Parses /proc/<pid>/cmdline and returns a list
        """
        with open("cmdline", opener=self._opener) as file:
            data = file.read()
        # Escape newlines
        data = data.replace("\n", "\\n")
        if data.endswith('\0'):
            return data.rstrip('\0').split('\0')
        return [data]

    @Property
    def comm(self):  # pylint: disable=method-hidden # https://github.com/PyCQA/pylint/issues/414
        """
        Parses /proc/comm
        """
        with open("comm", opener=self._opener) as file:
            data = file.read()
        # Strip trailing newline
        return data[:-1]

    @Property
    def environ(self):
        """
        Parses /proc/<pid>/environ and returns an AttrDict
        """
        with open("environ", opener=self._opener) as file:
            data = file.read()
        try:
            return AttrDict([_.split('=', 1) for _ in data[:-1].split('\0')])
        except ValueError:
            return data

    @Property
    def io(self):
        """
        Parses /proc/<pid>/io and returns an AttrDict
        """
        with open("io", opener=self._opener) as file:
            lines = file.read().splitlines()
        return AttrDict([_.split(': ') for _ in lines])

    @Property
    def limits(self):
        """
        Parses /proc/<pid>/limits and returns an AttrDict
        """
        with open("limits", opener=self._opener) as file:
            data = re.findall(
                r'^(.*?)\s{2,}(\S+)\s{2,}(\S+)', file.read(), re.M)[1:]
        return AttrDict(
            {_limits_fields[k]: AttrDict(zip(('soft', 'hard'), v))
             for (k, *v) in data})

    @Property
    def maps(self):
        """
        Parses /proc/<pid>/maps and returns a list of AttrDict's
        """
        with open("maps", opener=self._opener) as file:
            lines = file.read().splitlines()
        maps = [
            AttrDict(zip_longest(_maps_fields, line.split(maxsplit=5)))
            for line in lines]
        # From the proc(5) manpage:
        #  pathname is shown unescaped except for newline characters,
        #  which are replaced with an octal escape sequence. As a result,
        #  it is not possible to determine whether the original pathname
        #  contained a newline character or the literal \012 character sequence
        # So let's readlink() the address in the map_files directory
        for map_ in maps:
            if map_.pathname and "\\012" in map_.pathname:
                map_.pathname = os.readlink(
                    "map_files/%s" % map_.address,
                    dir_fd=self._dir_fd
                ).replace("\n", "\\n")
        return maps

    @Property
    def mounts(self):
        """
        Parses /proc/<pid>/mounts and returns a list of AttrDict's
        """
        with open("mounts", opener=self._opener) as file:
            lines = file.read().splitlines()
        return [
            AttrDict(zip(_mounts_fields, line.split()))
            for line in lines]

    @Property
    def smaps(self):
        """
        Parses /proc/<pid>/smaps and returns a list of AttrDict's
        """
        with open("smaps", opener=self._opener) as file:
            lines = file.read().splitlines()
        step = int(len(lines) / len(self.maps))
        maps = [
            {
                k: v.strip()
                for k, v in [_.split(':') for _ in lines[i + 1: i + step]]
            }
            for i in range(0, len(lines), step)]
        # USE this instead when support for Python 3.4 is dropped:
        # return [AttrDict(**a, **b) for a, b in zip(maps, self.maps)]
        return [AttrDict(a, **b) for a, b in zip(maps, self.maps)]

    @Property
    def stat(self):
        """
        Parses /proc/<pid>/stat and returns an AttrDict
        """
        with open("stat", opener=self._opener) as file:
            data = re.findall(r"\(.*\)|\S+", file.read()[:-1], re.M | re.S)
        info = AttrDict(zip(_stat_fields, data))
        # Remove parentheses
        info.comm = info.comm[1:-1]
        # Escape newlines
        info.comm = info.comm.replace("\n", "\\n")
        return info

    @Property
    def statm(self):
        """
        Parses /proc/<pid>/statm and returns an AttrDict
        """
        with open("statm", opener=self._opener) as file:
            data = map(int, file.read().split())
        return AttrDict(zip(_statm_fields, data))

    @Property
    def status(self):
        """
        Parses /proc/<pid>/status and returns an AttrDict
        """
        with open("status", opener=self._opener) as file:
            lines = file.read().splitlines()
        status = AttrDict([_.split(':\t') for _ in lines])
        status['Uid'] = AttrDict(
            zip(_status_XID_fields, map(int, status.Uid.split())))
        status['Gid'] = AttrDict(
            zip(_status_XID_fields, map(int, status.Gid.split())))
        # status['Name'] = status['Name'].replace("\\n", "\n")
        return status

    def __getitem__(self, path):
        if path in ('fd', 'map_files', 'task'):
            return self._lsdir(path)
        return super().__getitem__(path)

    def __missing__(self, path):
        """
        Creates dynamic attributes for elements in /proc/<pid>
        """
        if path in ('cmdline', 'comm', 'environ', 'io', 'limits',
                    'maps', 'mounts', 'smaps', 'stat', 'statm', 'status'):
            return getattr(self, path)
        return super().__missing__(path)
