#!/usr/bin/env python3
"""
Module SerialDispatcher -- Asynchronous Serial I/O
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains a basic asynchronous serial I/O
dispatcher.
"""

from plib.io.serial import SerialIOBase

from ._async import AsyncBase


class SerialDispatcher(SerialIOBase, AsyncBase):
    """Base "dispatcher" class for async serial I/O.
    """
    
    def __init__(self, devid=None, map=None):
        AsyncBase.__init__(self, map)
        SerialIOBase.__init__(self, devid)
    
    def set_port(self, port):
        SerialIOBase.set_port(self, port)
        self.set_fileobj(port, self._map)
    
    def close(self):
        AsyncBase.close(self)
        SerialIOBase.close(self)
