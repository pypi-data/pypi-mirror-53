#!/usr/bin/env python
"""
TEST.IO.TEST_PERSISTENT_NOPOLL.PY -- test script for sub-package IO of package PLIB
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This script contains unit tests for the persistent async I/O
classes in the PLIB.IO sub-package, with the poll function
disabled (so that select must be used).
"""

import unittest

from plib.io import async

from .testlib import PersistentTest
from .testlib_persistent import ReadWriteTestMixin, TerminatorTestMixin

async.use_poll(False)  # force use of select in all async loops


class XPersistentTestNoPoll(ReadWriteTestMixin, PersistentTest, unittest.TestCase):
    
    client_list = ["Python rocks!", "Try it today!", "You'll be glad you did!"]
    server_list = ["You betcha!", "It's *much* better than Perl!", "And don't even *mention* C++!"]


class XPersistentTestNoPollWithPush(XPersistentTestNoPoll):
    
    test_auto_push = True


class XPersistentTestLargeMessage1NoPoll(XPersistentTestNoPoll):
    
    client_list = ["a" * 6000, "b" * 6000, "c" * 6000]
    server_list = ["1" * 6000, "2" * 6000, "3" * 6000]


class XPersistentTestLargeMessage2NoPoll(XPersistentTestNoPoll):
    
    client_list = ["a" * 10000, "b" * 10000, "c" * 10000]
    server_list = ["1" * 10000, "2" * 10000, "3" * 10000]


class YPersistentTestNoPoll(TerminatorTestMixin, PersistentTest, unittest.TestCase):
    
    client_list = ["Python rocks!", "Try it today!", "You'll be glad you did!"]
    server_list = ["You betcha!", "It's *much* better than Perl!", "And don't even *mention* C++!"]


class YPersistentTestNoPollWithPush(YPersistentTestNoPoll):
    
    test_auto_push = True


class YPersistentTestLargeMessage1NoPoll(YPersistentTestNoPoll):
    
    client_list = ["a" * 6000, "b" * 6000, "c" * 6000]
    server_list = ["1" * 6000, "2" * 6000, "3" * 6000]


class YPersistentTestLargeMessage2NoPoll(YPersistentTestNoPoll):
    
    client_list = ["a" * 10000, "b" * 10000, "c" * 10000]
    server_list = ["1" * 10000, "2" * 10000, "3" * 10000]


if __name__ == '__main__':
    unittest.main()
