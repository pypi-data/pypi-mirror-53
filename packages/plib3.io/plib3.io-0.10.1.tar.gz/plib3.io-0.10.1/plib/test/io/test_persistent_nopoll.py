#!/usr/bin/env python3
"""
TEST.IO.TEST_PERSISTENT_NOPOLL.PY -- test script for sub-package IO of package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This script contains unit tests for the persistent async I/O
classes in the PLIB3.IO sub-package, with the poll function
disabled (so that select must be used).
"""

import unittest

from plib.io import nonblocking

from .testlib import PersistentTest
from .testlib_persistent import ReadWriteTestMixin, TerminatorTestMixin

nonblocking.use_poll(False)  # force use of select in all async loops


class XPersistentTestNoPoll(ReadWriteTestMixin, PersistentTest, unittest.TestCase):
    
    client_list = [b"Python rocks!", b"Try it today!", b"You'll be glad you did!"]
    server_list = [b"You betcha!", b"It's *much* better than Perl!", b"And don't even *mention* C++!"]


class XPersistentTestNoPollWithPush(XPersistentTestNoPoll):
    
    test_auto_push = True


class XPersistentTestLargeMessage1NoPoll(XPersistentTestNoPoll):
    
    client_list = [b"a" * 6000, b"b" * 6000, b"c" * 6000]
    server_list = [b"1" * 6000, b"2" * 6000, b"3" * 6000]


class XPersistentTestLargeMessage2NoPoll(XPersistentTestNoPoll):
    
    client_list = [b"a" * 10000, b"b" * 10000, b"c" * 10000]
    server_list = [b"1" * 10000, b"2" * 10000, b"3" * 10000]


class YPersistentTestNoPoll(TerminatorTestMixin, PersistentTest, unittest.TestCase):
    
    client_list = [b"Python rocks!", b"Try it today!", b"You'll be glad you did!"]
    server_list = [b"You betcha!", b"It's *much* better than Perl!", b"And don't even *mention* C++!"]


class YPersistentTestNoPollWithPush(YPersistentTestNoPoll):
    
    test_auto_push = True


class YPersistentTestLargeMessage1NoPoll(YPersistentTestNoPoll):
    
    client_list = [b"a" * 6000, b"b" * 6000, b"c" * 6000]
    server_list = [b"1" * 6000, b"2" * 6000, b"3" * 6000]


class YPersistentTestLargeMessage2NoPoll(YPersistentTestNoPoll):
    
    client_list = [b"a" * 10000, b"b" * 10000, b"c" * 10000]
    server_list = [b"1" * 10000, b"2" * 10000, b"3" * 10000]


if __name__ == '__main__':
    unittest.main()
