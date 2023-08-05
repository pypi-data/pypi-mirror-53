#!/usr/bin/env python3
"""
ECHO_SERVER.PY
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

Python implementation of an "echo" server, which simply
echoes back to each client what that client sends to it.

This class illustrates how the ``plib.io`` library
is set up to allow easy switching between different I/O
types (async, blocking, forking, and threading)--even, as
in this case, switching at runtime based on a command line
argument.

It also demonstrates the use of the ``SigIntServerMixin``
class in ``plib.io``, which provides a simple way for
a server do a controlled shutdown on a termination signal,
instead of printing a messy traceback (the Python default
on Ctrl-C) or just bailing without giving any of the
program's objects a chance to do exit-time processing.
"""

import sys
import os
import signal
import time

from plib.io.mixins import EchoRequestMixin, SigIntServerMixin
from plib.stdlib.imp import import_from_module


class EchoRequestHandlerMixin(EchoRequestMixin):
    """Echo request handler.
    
    Writes initial greeting message before starting
    round-trip data exchange.
    
    Echoes data received to stdout as well as back to client.
    
    Note that all code in this class works regardless of the
    I/O type.
    
    Note also that this class is written as a mixin so that
    the I/O type can be determined dynamically at run time.
    """
    
    keep_alive = True
    terminator = os.linesep.encode()  # so tools like netcat can talk to us
    echo_delay = 0
    
    def on_connect(self):
        # TerminatorReadWrite will automatically add
        # the line break when sending to client
        self.start(b"Connected to echo server.")
    
    def process_data(self):
        if self.read_data:
            # Add back line break when writing to stdout
            # since TerminatorReadWrite strips it
            sys.stdout.write("{}{}".format(self.read_data.decode(), os.linesep))
        if self.echo_delay:
            time.sleep(self.echo_delay)
        super(EchoRequestHandlerMixin, self).process_data()
    
    def on_close(self):
        sys.stdout.write("Echo server connection closed.{}".format(
                         os.linesep))


class EchoServerMixin(SigIntServerMixin):
    """Echo server.
    
    Adds some status messages to stdout for testing.
    
    Exits on Ctrl-C, neatly (i.e., without the messy traceback
    that Python would print if we used the default of letting
    Ctrl-C raise a KeyboardInterrupt).
    
    Note that this class is written as a mixin so that
    the I/O type can be determined dynamically at run time.
    """
    
    allow_reuse_address = True
    term_sigs = SigIntServerMixin.term_sigs + [signal.SIGTERM]
    
    def on_accept(self):
        sys.stdout.write("Echo server accepted connection.{}".format(
                         os.linesep))
    
    def serve_forever(self):
        sys.stdout.write("Echo server listening.{}".format(
                         os.linesep))
        super(EchoServerMixin, self).serve_forever()
    
    def server_close(self):
        super(EchoServerMixin, self).server_close()
        sys.stdout.write("Echo server exiting.{}".format(
                         os.linesep))


mixin_list = [
    (
        "EchoRequestHandler",
        "BaseRequestHandlerWithTerminator",
        ('echo_delay',)
    ),
    (
        "EchoServer",
        {
            "nonblocking": "SocketServer",
            "blocking": "SocketServer",
            "forking": "ForkingServer",
            "threading": "ThreadingServer"
        },
        ()
    )
]


def iopkg(iotype):
    if iotype in ("forking", "threading"):
        return "blocking"
    if iotype in ("nonblocking", "blocking"):
        return iotype
    raise ValueError("Invalid I/O type: {}".format(iotype))


if __name__ == '__main__':
    from plib.stdlib.options import parse_options
    
    optlist = (
        ("-d", "--echo-delay", {
            'action': "store", 'type': int,
            'dest': "echo_delay", 'default': 0,
            'help': "delay each echo by n seconds"
        }),
    )
    arglist = ["iotype"]
    
    opts, args = parse_options(optlist, arglist)
    
    thismod = sys.modules[__name__]
    for klassname, basename, attrnames in mixin_list:
        mixname = "{}Mixin".format(klassname)
        mixin = getattr(thismod, mixname)
        pkgname = iopkg(args.iotype)
        if isinstance(basename, dict):
            basename = basename[args.iotype]
        base = import_from_module(
            'plib.io.{}'.format(pkgname), basename)
        attrs = dict(
            (attrname, getattr(opts, attrname))
            for attrname in attrnames
        )
        klass = type(base)(klassname, (mixin, base), attrs)
        setattr(thismod, klassname, klass)
    
    EchoServer(("localhost", 7000), EchoRequestHandler).serve_forever()
