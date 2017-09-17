#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for inxwords.py
"""
from __future__ import print_function, unicode_literals
import unittest

import inxwords


class TestIt(unittest.TestCase):

    def test_none(self):
        intext = None
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 0)

    def test_not_found(self):
        intext = "#cymruambyth"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 0)

    def test_grammysin5words(self):
        intext = "#GrammysIn5Words"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 5)

    def test_myfeelingsinthreewords(self):
        intext = "#MyFeelingsInThreeWords"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 3)

    def test_infourwords(self):
        intext = "#SomethingInFourWords"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 4)

    def test_infivewords(self):
        intext = "#SomethingInFiveWords"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 5)

    def test_insixwords(self):
        intext = "#SomethingInSixWords"
        how_many = inxwords.ends_with_in_x_words(intext)
        self.assertEqual(how_many, 6)


if __name__ == '__main__':
    unittest.main()

# End of file
