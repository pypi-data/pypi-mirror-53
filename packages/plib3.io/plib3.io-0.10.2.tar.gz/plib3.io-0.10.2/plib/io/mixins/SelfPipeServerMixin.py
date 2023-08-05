#!/usr/bin/env python3
"""
Module SelfPipeServerMixin
Sub-Package IO.MIXINS of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the ``SelfPipeServerMixin`` class,
which provides "drop-in" usage of ``SelfPipe`` for
servers that conform to the PLIB3 I/O server API. The
``SocketServer`` class in ``plib.io.nonblocking`` uses
this class to implement the self-pipe trick.
"""

from plib.comm.classes import SelfPipe


class SelfPipeServerMixin(object):
    """Implements the self-pipe trick for PLIB3 servers.
    
    The ``pipe_class`` field stores the class that will be instantiated
    to create the pipe (an example is the async socket server, as
    noted above).
    """
    
    pipe_class = SelfPipe
    
    pipe = None
    
    def signal_callback(self, sig):
        # Override to process signals received when the pipe is triggered
        pass
    
    def server_start(self):
        super(SelfPipeServerMixin, self).server_start()
        self.pipe = self.pipe_class(self.signal_callback)
