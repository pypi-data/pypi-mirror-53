#!/usr/bin/env python3
"""
Module RequestBase
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous RequestBase class.
"""

from plib.io.socket import BaseRequest
from plib.io.nonblocking import SocketBase


class RequestBase(BaseRequest, SocketBase):
    """Base class for async request handler.
    """
    
    def __init__(self, request, client_addr, server):
        BaseRequest.__init__(self, request, client_addr, server)
        SocketBase.__init__(self, request)
        
        # If we're being called at all, we must be connected
        self.handle_connect()
