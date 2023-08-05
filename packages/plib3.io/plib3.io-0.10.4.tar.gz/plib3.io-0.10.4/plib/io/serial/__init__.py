#!/usr/bin/env python3
"""
Sub-Package IO.SERIAL of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This sub-package includes classes for handling serial
I/O channels. See the docstring for the parent package,
``plib.io``, for information on how this package
fits into the overall I/O package structure.
"""

from plib.stdlib.util import ModuleProxy

from ._serial import *

ModuleProxy(__name__).init_proxy(__name__, __path__, globals(), locals())

# Now clean up our namespace
del ModuleProxy
