#!/usr/bin/env python3
"""
TEST.IO.TESTLIB_NONBLOCKING.PY -- utility module for PLIB3 I/O tests
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains common code for the tests of the async
I/O modules in PLIB3.IO.
"""

from plib.io.mixins import EchoRequestMixin

import plib.io.nonblocking  # FIXME: why is this needed to make things work?

from plib.io.nonblocking import (
    SocketClient, BaseRequestHandler, SocketServer,
    SocketClientWithShutdown, BaseRequestHandlerWithShutdown,
    SocketClientWithTerminator, BaseRequestHandlerWithTerminator,
    SocketClientWithReadWrite, BaseRequestHandlerWithReadWrite
)

from .testlib import IOClientMixin, IOServerMixin


class AsyncClient(IOClientMixin, SocketClient):
    pass


class AsyncHandler(EchoRequestMixin, BaseRequestHandler):
    pass


class AsyncServer(IOServerMixin, SocketServer):
    pass


class AsyncTestMixin(object):
    
    client_class = AsyncClient
    handler_class = AsyncHandler
    server_class = AsyncServer


class AsyncShutdownClient(IOClientMixin,
                          SocketClientWithShutdown):
    pass


class AsyncShutdownHandler(EchoRequestMixin,
                           BaseRequestHandlerWithShutdown):
    pass


class AsyncShutdownTestMixin(object):
    
    client_class = AsyncShutdownClient
    handler_class = AsyncShutdownHandler
    server_class = AsyncServer


class AsyncTerminatorClient(IOClientMixin,
                            SocketClientWithTerminator):
    pass


class AsyncTerminatorHandler(EchoRequestMixin,
                             BaseRequestHandlerWithTerminator):
    pass


class AsyncTerminatorTestMixin(object):
    
    client_class = AsyncTerminatorClient
    handler_class = AsyncTerminatorHandler
    server_class = AsyncServer


class AsyncReadWriteClient(IOClientMixin,
                           SocketClientWithReadWrite):
    pass


class AsyncReadWriteHandler(EchoRequestMixin,
                            BaseRequestHandlerWithReadWrite):
    pass


class AsyncReadWriteTestMixin(object):
    
    client_class = AsyncReadWriteClient
    handler_class = AsyncReadWriteHandler
    server_class = AsyncServer
