#!/usr/bin/env python3
"""
Module SerialBase
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous SerialBase class.
"""

from plib.io.serial import SerialData
from plib.io.nonblocking import SerialDispatcher


class SerialBase(SerialData, SerialDispatcher):
    """Serial async I/O class with data handling.
    """
    pass
