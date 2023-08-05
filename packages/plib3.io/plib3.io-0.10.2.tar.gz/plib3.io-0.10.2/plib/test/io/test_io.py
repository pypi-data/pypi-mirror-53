#!/usr/bin/env python3
"""
TEST.IO.TEST_IO.PY -- test script for sub-package IO of package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This script contains basic unit tests for the I/O modules in the
PLIB3.IO sub-package.
"""

import unittest
import select

from plib.io import nonblocking

from .testlib import ClientServerTest, SmallBufferTest
from .testlib_blocking import *

# Only run async tests here if poll is available

if hasattr(select, 'poll'):
    
    nonblocking.use_poll(True)  # ensure we use poll (even if multiple test modules
                                # are being run that use async)
    
    from .testlib_nonblocking import *
    
    
    class NonBlockingSocketTest(AsyncTestMixin,
                                ClientServerTest,
                                unittest.TestCase):
        pass
    
    
    class NonBlockingSocketTestMultipleTrips(NonBlockingSocketTest):
        
        number_of_trips = 3
    
    
    class NonBlockingSocketTestLargeMessage1(NonBlockingSocketTest):
        
        test_data = b"a" * 6000
    
    
    class NonBlockingSocketTestLargeMessage2(NonBlockingSocketTest):
        
        test_data = b"a" * 10000
    
    
    class NonBlockingSocketTestBufsize(AsyncShutdownTestMixin,
                                       ClientServerTest,
                                       unittest.TestCase):
        
        test_data = b"x" * AsyncShutdownClient.bufsize
    
    
    class ReadWriteTest(AsyncReadWriteTestMixin,
                        ClientServerTest,
                        unittest.TestCase):
        pass
    
    
    class ReadWriteTestMultipleTrips(ReadWriteTest):
        
        number_of_trips = 3
    
    
    class ReadWriteTestLargeMessage1(ReadWriteTest):
        
        test_data = b"a" * 6000
    
    
    class ReadWriteTestLargeMessage2(ReadWriteTest):
        
        test_data = b"a" * 10000
    
    
    class ReadWriteTestBufsize(ReadWriteTest):
        
        # total data including read/write encoding should be exactly one buffer
        test_data = b"x" * (
            AsyncReadWriteClient.bufsize
            - len(str(AsyncReadWriteClient.bufsize))
            - len(AsyncReadWriteClient.bufsep)
        )
    
    
    class ReadWriteTestSmallBuffer(AsyncReadWriteTestMixin,
                                   SmallBufferTest,
                                   unittest.TestCase):
        pass
    
    
    class TerminatorTest(AsyncTerminatorTestMixin,
                         ClientServerTest,
                         unittest.TestCase):
        pass
    
    
    class TerminatorTestMultipleTrips(TerminatorTest):
        
        number_of_trips = 3
    
    
    class TerminatorTestLargeMessage1(TerminatorTest):
        
        test_data = b"a" * 6000
    
    
    class TerminatorTestLargeMessage2(TerminatorTest):
        
        test_data = b"a" * 10000
    
    
    class TerminatorTestBufsize(TerminatorTest):
        
        # total data including terminator should be exactly one buffer
        test_data = b"x" * (
            AsyncTerminatorClient.bufsize
            - len(AsyncTerminatorClient.terminator)
        )
    
    
    class TerminatorTestSmallBuffer(AsyncTerminatorTestMixin,
                                    SmallBufferTest,
                                    unittest.TestCase):
        pass


# Blocking tests run regardless of whether poll is available

class BlockingSocketTest(BlockingTestMixin,
                         ClientServerTest,
                         unittest.TestCase):
    pass


class BlockingSocketTestMultipleTrips(BlockingSocketTest):
    
    number_of_trips = 3


class BlockingSocketTestLargeMessage1(BlockingSocketTest):
    
    test_data = b"a" * 6000


class BlockingSocketTestLargeMessage2(BlockingSocketTest):
    
    test_data = b"a" * 10000


class BlockingSocketTestBufsize(BlockingShutdownTestMixin,
                                ClientServerTest,
                                unittest.TestCase):
    
    test_data = b"x" * BlockingShutdownClient.bufsize


class BlockingSocketTestReadWrite(BlockingReadWriteTestMixin,
                                  ClientServerTest,
                                  unittest.TestCase):
    pass


class BlockingSocketTestReadWriteMultipleTrips(BlockingSocketTestReadWrite):
    
    number_of_trips = 3


class BlockingSocketTestTerminator(BlockingTerminatorTestMixin,
                                   ClientServerTest,
                                   unittest.TestCase):
    pass


class BlockingSocketTestTerminatorMultipleTrips(BlockingSocketTestTerminator):
    
    number_of_trips = 3


if __name__ == '__main__':
    # Only print the message here so it won't print multiple times
    # if the test module gets re-imported (e.g., when running under
    # Windows in the forked server process); we do this similarly
    # in the other I/O test modules that print messages
    if not hasattr(select, 'poll'):
        print("Poll not available, skipping nonblocking I/O tests for poll.")
    unittest.main()
