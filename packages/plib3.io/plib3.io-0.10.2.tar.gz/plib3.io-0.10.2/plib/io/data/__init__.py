#!/usr/bin/env python3
"""
Sub-Package IO.DATA of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This sub-package includes classes for customized data
handling for any I/O mode and channel type. See the
docstring for the parent package, ``plib.io``,
for information on how this package fits into the overall
I/O package structure.
"""

from plib.stdlib.util import ModuleProxy

ModuleProxy(__name__).init_proxy(__name__, __path__, globals(), locals())

# Now clean up our namespace
del ModuleProxy
