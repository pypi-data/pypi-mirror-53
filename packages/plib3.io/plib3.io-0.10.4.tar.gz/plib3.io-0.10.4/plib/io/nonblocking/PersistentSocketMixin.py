#!/usr/bin/env python3
"""
Module PersistentSocketMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous PersistentSocketMixin class;
this class is factored out from PersistentSocketClient so that alternate
read/write handling can be mixed in.
"""

from plib.io.socket import ConnectMixin
from plib.io.nonblocking import AsyncConnectMixin, PersistentMixin


class PersistentSocketMixin(AsyncConnectMixin, ConnectMixin, PersistentMixin):
    """Mixin class for persistent, full-duplex asynchronous socket I/O.
    
    Can be used for both clients and servers, but intended
    mainly for clients that need connect functionality. (For
    server-side persistent sockets, you should normally use the
    ``PersistentRequestHandler`` class with ``SocketServer``.)
    """
    pass
