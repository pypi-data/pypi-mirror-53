#!/usr/bin/env python3
"""
Module SerialServerMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous SerialServerMixin class.
"""

from plib.io.serial import BaseServer
from plib.io.nonblocking import ServerMixin


class SerialServerMixin(BaseServer, ServerMixin):
    """Asynchronous server-side serial I/O mixin class.
    """
    pass
