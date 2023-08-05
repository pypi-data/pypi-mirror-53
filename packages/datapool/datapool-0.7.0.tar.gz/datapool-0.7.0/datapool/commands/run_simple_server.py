#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import glob
import os
import queue
import signal
import threading
import time

from prometheus_client import Gauge

from datapool.dispatcher import Dispatcher
from datapool.instance.config_handling import read_config
from datapool.instance.landing_zone_structure import lock_file

from ..database import check_if_tables_exist, setup_db
from ..errors import InvalidOperationError
from ..http_server import DataPoolHttpServer, port_is_in_use
from ..logger import get_cmdline_logger
from ..observer import CREATED_EVENT, MODIFIED_EVENT, shutdown_observer, start_observer
from ..utils import (
    EnhancedThread,
    install_signal_handler_for_debugging,
    is_server_running,
    remove_pid_file,
    write_pid_file,
)

queue_size = Gauge("dp_queue_size", "number of files in queue waiting to be processed")


def run_simple_server(
    verbose, print_ok, print_err, schedule_existing_files=True, still_running=None
):

    """setting signal handlers only works when run in main thread,
       in testing we want to run the server in the background thread."""

    config = read_config()
    if config is None:
        print_err("- no config file found. please run 'whdp init-config' " "first.")
        return 1

    if is_server_running(config):
        print_err(
            "- found pid file at {!r}, seems like server is already running.".format(
                config.server.pid_file
            )
        )
        print_err(
            "- this could also be a relict from a crash. so delete it if you"
            " know what you are doing."
        )
        return 1

    port = config.http_server.port
    if port_is_in_use(port):
        print_err("- the port {} for the http server is already in use.".format(port))
        return 1

    with get_cmdline_logger(verbose):

        _setup(config, print_ok, print_err, verbose)

        write_pid_file(config)
        dispatcher, threads = _start_threads(
            config, print_ok, print_err, schedule_existing_files
        )

        def shutdown(signum=None, frame=None):
            nonlocal still_running

            if not signum:  # keyboardinterrupt
                return

            print_err("- received signal {}".format(signum or "UNKNOWN"))
            still_running = lambda: False  # noqa

        for sig in (signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, shutdown)

        try:
            while still_running is None or still_running():
                time.sleep(.01)
        except KeyboardInterrupt:
            print_ok("")
            print_err("- got keyboard interrupt")
            still_running = lambda: False  # noqa

        _shutdown_threads(threads)
        dispatcher.engine.dispose()
        print_ok("+ done", fg="green")

        return 0


def _setup(config, print_ok, print_err, verbose):
    try:
        already_setup = check_if_tables_exist(config.db)
    except InvalidOperationError as e:
        print_err("+ can not check database: {}".format(e))
        return 1
    if not already_setup:
        print_ok("- setup fresh db")
        try:
            setup_db(config.db, verbose=verbose)
        except InvalidOperationError as e:
            print_err("+ can not setup database: {}".format(e))
            return 1
    else:
        print_ok("- db already setup")

    if config.julia.executable:

        print_ok("- check startup julia")
        from datapool.julia_runner import JuliaRunner

        r = JuliaRunner(config.julia.executable)
        r.start_interpreter()
        ok = r.is_alive()
        if not ok:
            print_err("+ julia startup failed")
            return 1


def _start_threads(config, print_ok, print_err, schedule_existing_files):

    dispatcher = Dispatcher(config, info=print_ok)
    q = queue.Queue()
    root_folder = config.landing_zone.folder

    if schedule_existing_files:
        print_ok("- put existing files in dispatch queue")
        _enqueue_existing_files(q, root_folder)

    time.sleep(.2)

    observer = Observer(q, root_folder, print_ok, print_err)
    observer.start()
    time.sleep(.2)

    http_server = DataPoolHttpServer(config.http_server.port, print_ok)
    http_server.start()
    time.sleep(.2)

    main_loop = MainLoop(config, dispatcher, q, print_ok, print_err)
    main_loop.start()

    threads = [main_loop, observer, http_server]

    install_signal_handler_for_debugging()
    print_ok("- installed signale handler")
    print_ok(
        "  run 'kill -SIGUSR1 {}' to get tracebacks of all running threads".format(
            os.getpid()
        )
    )

    return dispatcher, threads


def _enqueue_existing_files(q, root_folder):
    pathes = glob.glob(os.path.join(root_folder, "**/*.raw"), recursive=True)

    def sort_key(path):
        print(path, os.path.basename(path))
        file_name_stem = os.path.splitext(os.path.basename(path))[0]
        return file_name_stem.split("-")[1]

    pathes.sort(key=sort_key)

    for path in pathes:
        q.put((CREATED_EVENT, path, time.time()))


class MainLoop(EnhancedThread):
    def __init__(self, config, dispatcher, q, print_ok, print_err):
        self.config = config
        self.dispatcher = dispatcher
        self.q = q
        self.running = True
        self.print_ok = print_ok
        self.print_err = print_err
        self._dispatching = False
        super().__init__()

    def task(self):
        self.print_ok("- main loop ready to dispatch incoming files")
        try:

            while self.running:
                try:
                    __, rel_path, timestamp = self.q.get(timeout=.01)
                except queue.Empty:
                    continue

                queue_size.set(self.q.qsize())

                self._dispatching = True
                self.print_ok("- dispatch {}".format(rel_path))
                results = self.dispatcher.dispatch(rel_path, timestamp)
                for result in results:
                    if isinstance(result, str):
                        self.print_ok("  {}".format(result))
                    else:
                        self.print_err("  error: {}".format(result))
                self.print_ok("  dispatch done")
                self._dispatching = False
                queue_size.set(self.q.qsize())
        finally:
            remove_pid_file(self.config)

    def stop(self):
        if self._dispatching:
            self.print_ok("- main loop waits for dispatcher to finish.")
            while self._dispatching:
                time.sleep(.1)
        self.print_ok("- shutdown main loop")
        self.running = False
        self.join()
        self.print_ok("- main loop shut down")


class Observer:
    def __init__(self, q, root_folder, print_ok, print_err):
        self.q = q
        self.root_folder = root_folder
        self.print_ok = print_ok
        self.print_err = print_err

    def _call_back(self, event, rel_path, timestamp):
        if os.path.basename(rel_path).startswith("."):
            return
        if event not in (CREATED_EVENT, MODIFIED_EVENT):
            if rel_path == lock_file:
                self.print_ok("- removed update lock for landing zone")
        else:
            if rel_path == lock_file:
                self.print_ok("- lock landing zone for updating")
            else:
                self.q.put((event, rel_path, timestamp))

    def start(self):
        try:
            self.observer = start_observer(self.root_folder, self._call_back)
        except Exception as e:
            self.print_err("- could not start observer: {}".format(e))
            return 1
        self.print_ok("- started observer")
        self.print_ok("- observe {} now".format(self.root_folder))
        return 0

    def stop(self):
        self.print_ok("- shutdown observer")
        shutdown_observer(self.observer)
        self.print_ok("- observer shutdown")


def _shutdown_threads(threads):

    main_loop, observer, http_server = threads

    http_server.stop()
    observer.stop()
    main_loop.stop()
