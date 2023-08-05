import argparse
# TODO: gracefully handle platforms that don't support fcntl
import fcntl
import functools
import logging
import inspect
import os
import shlex
import signal
import subprocess
import sys
import tempfile
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@contextmanager
def ignore(sig_n):
    handler = signal.getsignal(sig_n)
    signal.signal(sig_n, signal.SIG_IGN)
    try:
        yield
    finally:
        signal.signal(sig_n, handler)


def handler(callback, folders, *args):
    with ignore(signal.SIGIO):
        callback()

        # Re-watch in case a directory was added
        # TODO: Handle directory removal
        rewatch(folders)


def install_handler(callback):
    # for updated files
    signal.signal(signal.SIGIO, callback)


watched = []


def rewatch(folders):
    for fd in watched:
        try:
            os.close(fd)
        except:
            pass
    watch(folders)


# adapted from https://stackoverflow.com/a/473471
def watch(directories):
    paths = set()
    for directory in directories:
        for d, _, _ in os.walk(directory):
            paths.add(d)

    for path in paths:
        fd = os.open(path, os.O_RDONLY)
        fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
        fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)
        watched.append(fd)


class Executor(object):
    """
    Handles running commands.
    """
    def __init__(self, specs):
        self.specs = specs

    def run(self, _):
        """
        Execute cmd based on spec provided at construction.
        Args:
            (*) disregarded
        Returns:
            (bool) true on success
        """
        print('#' * 40)
        for d in self.specs:
            if not self.run_command(d):
                return False
        return True

    def run_command(self, spec):
        print('-' * 40)
        if spec.command is None:
            print('No command defined, skipping.')
            return True
        print('Running {} in {} @ {}'.format(
            spec.command, spec.folder, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        rc = subprocess.call(spec.command, shell=True, cwd=spec.folder)
        if rc:
            return False
        else:
            print('SUCCESS')
            return True


def fn_sequence(*fns):
    def inner():
        result = fns[0](True)
        for f in fns[1:]:
            result = f(result)
    return inner


def success_command(command):
    def inner(result):
        args = [command]
        if result:
            args.append('1')
        else:
            args.append('0')
        subprocess.call(args)
    return inner


Spec = namedtuple('Spec', ['folder', 'command'])
def parse_specs(specs):
    out = []
    for spec in specs:
        try:
            folder, command = spec.split(':', 1)
        except ValueError:
            # TODO: Error on missing folders
            folder, command = spec, None
        out.append(Spec(folder, command))
    return out


def main():
    parser = argparse.ArgumentParser(description='''
        Watch contents of directories and execute rebuild when finished.
        ''')
    parser.add_argument('--start-command', help='''
        Command to execute when build is initiated.
        ''')
    parser.add_argument('--result-command', help='''
        Command to execute on success or failure. Argument will be 1 for
        success or 0 for failure.
        ''')
    parser.add_argument('specs', nargs='+', metavar='DIR', help='''
        Directory/command specifications, in the format
        
            dir:cmd

        if cmd is not provided then nothing is executed.
        ''')
    args = parser.parse_args()
    specs = parse_specs(args.specs)
    dirs = [s.folder for s in specs if s.folder]
    for d in dirs:
        if not os.path.exists(d):
            print('{} does not exist'.format(d))
            sys.exit(1)
    
    commands = []
    if args.start_command:
        # TODO: shell=True
        commands.append(lambda _: subprocess.call(args.start_command))
    # TODO: Execute from the single indexed item onwards
    builder = Executor(specs)
    commands.append(builder.run)
    if args.result_command:
        commands.append(success_command(args.result_command))
    on_io = fn_sequence(*commands)
    callback = functools.partial(handler, on_io, dirs)
    install_handler(callback)
    watch(dirs)
    # Allow manually invoking.
    while True:
        try:
            # TODO: Dedicated console logger separate from debug
            logger.info('Waiting...')
            input()
            logger.info('Starting manually...')
            callback()
        except KeyboardInterrupt:
            logger.info('Exiting...')
            break
