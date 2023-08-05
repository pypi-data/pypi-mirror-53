#!/usr/bin/env python3
"""
TEST.IO.TEST_NOPOLL.PY -- test script for sub-package IO of package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This script contains unit tests for the async I/O modules in
the PLIB3.IO sub-package, with the poll function disabled
(so that select must be used).
"""

import unittest

from plib.io import nonblocking

from .testlib import ClientServerTest, SmallBufferTest
from .testlib_nonblocking import *

nonblocking.use_poll(False)  # force use of select in all async loops


class NonBlockingSocketTestNoPoll(AsyncTestMixin,
                                  ClientServerTest,
                                  unittest.TestCase):
    pass


class NonBlockingSocketTestNoPollMultipleTrips(NonBlockingSocketTestNoPoll):
    
    number_of_trips = 3


class NonBlockingSocketTestLargeMessage1NoPoll(NonBlockingSocketTestNoPoll):
    
    test_data = b"a" * 6000


class NonBlockingSocketTestLargeMessage2NoPoll(NonBlockingSocketTestNoPoll):
    
    test_data = b"a" * 10000


class NonBlockingSocketTestBufsizeNoPoll(AsyncShutdownTestMixin,
                                         ClientServerTest,
                                         unittest.TestCase):
    
    test_data = b"x" * AsyncShutdownClient.bufsize


class ReadWriteTestNoPoll(AsyncReadWriteTestMixin,
                          ClientServerTest,
                          unittest.TestCase):
    pass


class ReadWriteTestNoPollMultipleTrips(ReadWriteTestNoPoll):
    
    number_of_trips = 3


class ReadWriteTestLargeMessage1NoPoll(ReadWriteTestNoPoll):
    
    test_data = b"a" * 6000


class ReadWriteTestLargeMessage2NoPoll(ReadWriteTestNoPoll):
    
    test_data = b"a" * 10000


class ReadWriteTestBufsizeNoPoll(ReadWriteTestNoPoll):
    
    # total data including read/write encoding should be exactly one buffer
    test_data = b"x" * (
        AsyncReadWriteClient.bufsize
        - len(str(AsyncReadWriteClient.bufsize))
        - len(AsyncReadWriteClient.bufsep)
    )


class ReadWriteTestSmallBufferNoPoll(AsyncReadWriteTestMixin,
                                     SmallBufferTest,
                                     unittest.TestCase):
    pass


class TerminatorTestNoPoll(AsyncTerminatorTestMixin,
                           ClientServerTest,
                           unittest.TestCase):
    pass


class TerminatorTestNoPollMultipleTrips(TerminatorTestNoPoll):
    
    number_of_trips = 3


class TerminatorTestLargeMessage1NoPoll(TerminatorTestNoPoll):
    
    test_data = b"a" * 6000


class TerminatorTestLargeMessage2NoPoll(TerminatorTestNoPoll):
    
    test_data = b"a" * 10000


class TerminatorTestBufsizeNoPoll(TerminatorTestNoPoll):
    
    # total data including terminator should be exactly one buffer
    test_data = b"x" * (
        AsyncTerminatorClient.bufsize
        - len(AsyncTerminatorClient.terminator)
    )


class TerminatorTestSmallBufferNoPoll(AsyncTerminatorTestMixin,
                                      SmallBufferTest,
                                      unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
