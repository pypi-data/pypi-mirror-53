#!/usr/bin/env python3
"""
Module ThreadingServer
Sub-Package IO.BLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the ``ThreadingServer`` class, which
is a threading version of the blocking I/O socket server.
See the module docstring for the base class, ``SocketServer``,
for more information.
"""

from plib.comm._threadwrapper import ThreadWrapper

from plib.io.blocking import SocketServer
from plib.io.mixins import ChildWrapperMixin


class ThreadingServer(ChildWrapperMixin, SocketServer):
    """Threading TCP server.
    
    This server creates a new thread to handle each request.
    """
    
    wrapper_class = ThreadWrapper
