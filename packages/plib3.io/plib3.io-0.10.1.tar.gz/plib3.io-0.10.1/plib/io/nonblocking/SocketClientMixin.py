#!/usr/bin/env python3
"""
Module SocketClientMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous SocketClientMixin class;
this class is factored out from SocketClient so that alternate
read/write handling can be mixed in.
"""

from plib.io.socket import BaseClient
from plib.io.nonblocking import AsyncConnectMixin, ClientMixin


class SocketClientMixin(AsyncConnectMixin, BaseClient, ClientMixin):
    """Asynchronous socket client mixin class.
    """
    pass
