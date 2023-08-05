#!/usr/bin/env python3
"""
Module ClientMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous ClientMixin class.
"""

from plib.io.nonblocking import AsyncCommunicator
from plib.io.comm import ClientCommunicator


class ClientMixin(AsyncCommunicator, ClientCommunicator):
    """Mixin class for async client-side I/O channel.
    """
    
    def run_wait_loop(self, obj, attrname):
        def callback():
            if getattr(obj, attrname):
                return False
        self.do_loop(callback)
