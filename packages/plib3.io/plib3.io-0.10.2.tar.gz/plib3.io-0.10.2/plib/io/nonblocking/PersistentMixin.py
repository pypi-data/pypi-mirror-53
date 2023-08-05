#!/usr/bin/env python3
"""
Module PersistentMixin
Sub-Package IO.NONBLOCKING of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the asynchronous PersistentMixin class.
"""

from plib.io.nonblocking import AsyncCommunicator
from plib.io.comm import PersistentCommunicator


class PersistentMixin(AsyncCommunicator, PersistentCommunicator):
    pass
