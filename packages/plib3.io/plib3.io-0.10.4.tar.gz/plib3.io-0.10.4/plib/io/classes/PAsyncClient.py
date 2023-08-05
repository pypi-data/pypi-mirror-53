#!/usr/bin/env python3
"""
Module PAsyncClient
Sub-Package IO.CLASSES of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the ``PAsyncClient`` class. This is an
asynchronous socket I/O client using the ``PClientBase``
interface.
"""

from plib.io.nonblocking import SocketClient
from plib.io.classes import PClientBase


class PAsyncClient(PClientBase, SocketClient):
    """Asynchronous TCP client class.
    
    Connects with TCP server, writes data, and stores the
    result. See the ``PClientBase`` docstring for more
    information.
    """
    pass
