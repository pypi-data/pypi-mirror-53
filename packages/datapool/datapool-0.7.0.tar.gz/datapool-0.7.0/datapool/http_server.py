#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import importlib
import json
import socket
import subprocess

# Copyright © 2018 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
from contextlib import contextmanager
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread

from prometheus_client.exposition import MetricsHandler

from .logger import logger
from .utils import EnhancedThread


def _get_logs(n):
    p = subprocess.Popen(
        "journalctl -u {name} -n {n}".format(name=__package__, n=n),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    output = p.stdout.readlines()
    return output


@contextmanager
def patch_get_logs(function):
    globals()["_get_logs"] = function
    try:
        yield
    finally:
        globals()["_get_logs"] = _get_logs


def latest_logs(n=1000):
    output = _get_logs(n)
    # includes code to automatically scroll down in browser, incl.
    # scroll down after reload. see also
    # https://stackoverflow.com/questions/3664381
    result = b"""
    <html>
        <body>
            <pre>
            %s
            </pre>
            <div id="end" />
        </body>

        <script>
             window.onload = function() {
                    var element = document.getElementById("end");
                    element.scrollTop = element.scrollHeight;
                    element.scrollIntoView(false);
                    console.log(element);
                };
             window.onbeforeunload  = window.onload;
        </script>
    </html>
""" % (
        b"".join(output),
    )
    return result


class _Handler(BaseHTTPRequestHandler):

    # Needed to work together with prometheus:
    registry = MetricsHandler.registry

    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        self._print_ok = print

    def do_GET(self):

        if self.path == "/metrics":
            return MetricsHandler.do_GET(self)

        elif self.path == "/logs":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(latest_logs())

        elif self.path.startswith("/logs/"):
            try:
                n = int(self.path.split("/")[2])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(latest_logs(n))

        elif self.path == "/":

            version = importlib.import_module(__package__).__version__
            message = dict(status="alive", version=version, started=self.server.started)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(message), "utf-8"))

        else:
            self.send_error(404)

    def log_message(self, format_, *args):
        if args and isinstance(args[0], str):
            path = args[0].split(" ")[1]
            if path == "/metrics":
                return
            self._print_ok("- http server received {}".format(format_ % args))

    @staticmethod
    def _set_print_ok(print_ok):
        _Handler._print_ok = print_ok


class _ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """Thread per request HTTP server."""

    # Make worker threads "fire and forget". Beginning with Python 3.7 this
    # prevents a memory leak because ``ThreadingMixIn`` starts to gather all
    # non-daemon threads in a list in order to join on them at server close.
    # Enabling daemon threads virtually makes ``_ThreadingSimpleServer`` the
    # same as Python 3.7's ``ThreadingHTTPServer``.
    daemon_threads = True

    def __init__(self, address, handler, print_ok):
        handler._set_print_ok(print_ok)
        HTTPServer.__init__(self, address, handler)
        self.started = str(datetime.now())


class DataPoolHttpServer:
    def __init__(self, port=8000, print_ok=print):
        self.port = port
        self.thread = None
        self.httpd = None
        self.print_ok = print_ok

    def start(self):
        self.print_ok("- start http server on port {}".format(self.port))
        server_address = ("", self.port)
        httpd = _ThreadingSimpleServer(server_address, _Handler, self.print_ok)
        thread = Thread(target=httpd.serve_forever)
        thread.start()
        self.thread = thread
        self.httpd = httpd
        logger().info("started web server")

    def stop(self):
        if self.thread is None or self.httpd is None:
            raise RuntimeError("you must start server first.")

        if not self.thread.isAlive():
            raise RuntimeError("something went wrong when starting webserver.")
        self.print_ok("- stop http server")

        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join()
        logger().info("web server shut down")
        self.print_ok("- stopped http server")


def port_is_in_use(port):
    # from https://stackoverflow.com/questions/2470971

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
