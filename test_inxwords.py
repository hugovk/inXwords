#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for inxwords.py
"""
from __future__ import print_function, unicode_literals
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import inxwords


class TestIt(unittest.TestCase):

    def test_grammysin5words(self):
        intext = "#GrammysIn5Words"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 5)

    def test_myfeelingsinthreewords(self):
        intext = "#MyFeelingsInThreeWords"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 3)


if __name__ == '__main__':
    unittest.main()

# End of file
