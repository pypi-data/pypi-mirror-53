#!/usr/bin/env python3
"""
Module UTILS -- I/O class utilities
Sub-Package IO of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains utility functions and classes for
use by the I/O sub-packages. The main ones intended
for external use are:

- Class ``IOModuleProxy``: implements the machinery for
  constructing I/O classes with alternate read/write
  handling on the fly. See the ``plib.io``
  sub-package docstring for an overview of this topic.

- function ``io_class``: the underlying function used by
  ``IOModuleProxy`` to work its magic; it is exposed so
  that, if all else fails, you can call the machinery
  directly.

- global variable ``io_meta``: the metaclass used to
  construct the I/O classes on the fly. It should be very,
  very rare that you need to change this from its default
  of ``type``.
"""

from itertools import chain

from plib.stdlib.util import ModuleProxy
from plib.stdlib.imp import import_from_module


# Machinery to add the "standard" I/O mixin classes to the
# nonblocking and blocking I/O sub-package namespaces

def modname_from_pkgname(pkgname):
    return pkgname.split('.')[-1]


def format_doc(doc, pkgname):
    if '{}' in doc:
        return doc.format(modname_from_pkgname(pkgname))
    return doc


def mixin_helper(pkgname, klassname, bases, doc):
    def f():
        baselist = [
            import_from_module(pkgname, basename)
            for basename in bases
        ]
        return type(klassname, tuple(baselist), {
            '__module__': pkgname,
            '__doc__': format_doc(doc, pkgname)
        })
    f.__name__ = "{}_{}_helper".format(modname_from_pkgname(pkgname), klassname)
    return f


_BaseRequestHandler_doc = """
    Basic {} request handler; default is to do one
    round-trip exchange of data and then shut down.
    """

_SerialClient_doc = """
    Basic {} serial device client class. Call the
    ``client_communicate`` method to open a serial device
    and send data; override the ``process_data`` method to
    do something with the reply.
    """

_SerialServer_doc = """
    Basic {} serial device server class. Call the
    ``serve_forever`` method to run the server. Note that the
    default is to remain open for an unlimited number of
    round-trip data exchanges; override the ``query_done`` method
    to determine when the server should close.
    """

_SocketClient_doc = """
    Basic {} socket client class. Call the
    ``client_communicate`` method to connect to a server
    and send data; override the ``process_data`` method to
    do something with the reply.
    """

_mixin_names = [
    ('BaseRequestHandler', ('ServerMixin', 'RequestBase'), _BaseRequestHandler_doc),
    ('SerialClient', ('SerialClientMixin', 'SerialBase'), _SerialClient_doc),
    ('SerialServer', ('SerialServerMixin', 'SerialBase'), _SerialServer_doc),
    ('SocketClient', ('SocketClientMixin', 'SocketBase'), _SocketClient_doc)
]

_PersistentRequestHandler_doc = """
    Base class for persistent, full-duplex asynchronous socket
    request handler.
    """

_PersistentSerial_doc = """
    Base class for persistent, full-duplex asynchronous serial
    device I/O. Can be used for both clients and servers.
    """

_PersistentSocket_doc = """
    Base class for persistent, full-duplex asynchronous socket
    I/O. Can be used for both clients and servers, but intended
    mainly for clients that need connect functionality. (For
    server-side persistent sockets, you should normally use the
    ``PersistentRequestHandler`` class with ``SocketServer``.)
    """

_persistent_names = [
    ('PersistentRequestHandler', ('PersistentMixin', 'RequestBase'), _PersistentRequestHandler_doc),
    ('PersistentSerial', ('PersistentMixin', 'SerialBase'), _PersistentSerial_doc),
    ('PersistentSocket', ('PersistentSocketMixin', 'SocketBase'), _PersistentSocket_doc)
]


def _get_names(add_persistent):
    """ Return the list of mixin class name entries to be used. """
    
    if add_persistent:
        return chain(_mixin_names, _persistent_names)
    return _mixin_names


def _get_mixin_names(pkgname, add_persistent):
    """Return "standard" mixin entries for I/O classes in pkgname.
    
    This means we don't have to have "boilerplate" .py module files
    in sub-packages for classes that are simple mixins.
    """
    
    return dict(
        (klassname, mixin_helper(pkgname, klassname, bases, doc))
        for klassname, bases, doc in _get_names(add_persistent)
    )


# Specialized ModuleProxy that can generate alternate read/write
# classes on the fly; this allows you to append 'WithShutdown',
# 'WithTerminator', or 'WithReadWrite' to a valid class name from
# above and have the appropriate read/write handling class spliced
# into the base class list for the class you've requested. This is
# nice because now you don't have to remember exactly where in the
# MRO the read/write class has to go to work properly; that's all
# done automatically. (Note that we allow for the possibility--very
# unlikely, we hope--that someone might want to use a custom
# metaclass to construct these classes; hence the io_meta global
# and the meta parameter to io_class.)

_readwrite_doc = """
    Uses the {} data handling mixin class.
    """

_rwbases = {
    'WithShutdown': 'ShutdownReadWrite',
    'WithTerminator': 'TerminatorReadWrite',
    'WithReadWrite': 'ReadWrite'
}

io_meta = type


def io_class(pkgname, name, rwbase, add_persistent=False, endstr="", meta=None):
    """
    Return a modified version of class ``name`` from package ``pkgname``
    with alternate read/write class ``rwbase`` spliced into its base
    class list. If ``add_persistent``, include the "persistent" class
    names in the validity check for ``name``; if ``endstr``, append
    that string to the name of the created class (instead of the default
    based on ``rwbase.__name__``); if ``meta`` is not ``None``, use the
    given metaclass to create the class to be returned (instead of the
    default stored in the ``io_meta`` global).
    """
    
    for klassname, bases, doc in _get_names(add_persistent):
        if klassname == name:
            base1, base2 = [
                import_from_module(pkgname, base)
                for base in bases
            ]
            if not endstr:
                endstr = "With{}".format(rwbase.__name__)
            rwdoc = _readwrite_doc.format(rwbase.__name__)
            if meta is None:
                meta = io_meta
            return meta(klassname + endstr,
                        (base1, rwbase, base2),
                        {
                            '__module__': pkgname,
                            '__doc__': format_doc(doc + rwdoc, pkgname)
                        })
    raise ValueError("IO class {} not found".format(name))


class IOModuleProxy(ModuleProxy):
    # ``ModuleProxy`` subclass that adds the ability to construct
    # alternate read/write classes on the fly, so that they can
    # appear in the module namespace.
    
    def init_proxy(self, pkgname, path, globals_dict, locals_dict,
                   names=None, excludes=None, autodiscover=True,
                   add_persistent=False, meta=None):
        
        self._mixin_names = _get_mixin_names(pkgname, add_persistent)
        self._rw_names = dict(
            ('{}{}'.format(basename, rwsuffix), rwsuffix)
            for basename in self._mixin_names
            for rwsuffix in _rwbases.keys()
        )
        ModuleProxy.init_proxy(self, pkgname, path,
                               globals_dict, locals_dict,
                               names=names, excludes=excludes,
                               autodiscover=autodiscover)
        self.add_persistent = add_persistent
        self.meta = meta
    
    def __dir__(self):
        return sorted(dir(self._mod) + self._realized_names
                      + list(self._names.keys())
                      + list(self._mixin_names.keys())
                      + list(self._rw_names.keys()))
    
    def _get_name(self, name, module=None):
        result = super(IOModuleProxy, self)._get_name(name, module)
        if result is self.not_proxied:
            mnames = self._mixin_names
            rwnames = self._rw_names
            
            if name in mnames:
                result = mnames[name]()  # we know it's a helper so just call it
                self._realize_name(name, result)
                del mnames[name]
            
            elif name in rwnames:
                endstr = rwnames[name]
                assert name.endswith(endstr)
                basename = name[:-len(endstr)]
                
                rwbase = import_from_module(
                    'plib.io.data', _rwbases[endstr])
                result = self.get_readwrite_class(
                    basename, rwbase, endstr)
                
                self._realize_name(name, result)
                del rwnames[name]
        
        return result
    
    def get_readwrite_class(self, basename, rwklass, endstr=""):
        """
        Returns an alternate to valid I/O class ``basename`` with the
        read/write handling class ``rwklass`` spliced into its MRO. This
        allows access to the same machinery as ``IOModuleProxy`` uses
        for alternate read/write handling classes.
        """
        
        return io_class(self._mod.__name__, basename, rwklass,
                        self.add_persistent, endstr, self.meta)
