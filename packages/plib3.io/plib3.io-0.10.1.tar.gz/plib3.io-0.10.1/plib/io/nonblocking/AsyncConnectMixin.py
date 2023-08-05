#!/usr/bin/env python3
"""
Module AsyncConnectMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous AsyncConnectMixin class.
"""


class AsyncConnectMixin(object):
    """Mixin class to enable async client connect functionality.
    
    Overrides the ``writable`` and ``readable`` methods to return
    ``True`` if a connect is pending (to make sure we get notified
    when the asynchronous connect completes; it could be either a
    read or a write ``select()`` return so we allow for both to
    be safe).
    """
    
    def writable(self):
        return self.connect_pending or \
            super(AsyncConnectMixin, self).writable()
    
    def readable(self):
        return self.connect_pending or \
            super(AsyncConnectMixin, self).readable()
