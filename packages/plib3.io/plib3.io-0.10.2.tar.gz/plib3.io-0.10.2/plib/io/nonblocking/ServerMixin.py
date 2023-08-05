#!/usr/bin/env python3
"""
Module ServerMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous ServerMixin class.
"""

from plib.io.nonblocking import AsyncCommunicator
from plib.io.comm import ServerCommunicator


class ServerMixin(AsyncCommunicator, ServerCommunicator):
    """Mixin class for async server-side I/O channel.
    """
    pass
