import unittest

from color_parser import parse_color


class TestColorParse(unittest.TestCase):

    def test_black_is_correct(self):
        self.assertEqual((0, 0, 0), parse_color('#000000'))

    def test_white_is_correct(self):
        self.assertEqual((255, 255, 255), parse_color('#FFFFFF'))

    def test_green_is_correct(self):
        self.assertEqual((0, 255, 0), parse_color('#00ff00'))

    def test_initial_hash_is_optional(self):
        self.assertEqual((0, 255, 0), parse_color('00ff00'))

    def test_invalid_throws(self):
        self.assertRaises(ValueError, parse_color, '#000')
        self.assertRaises(ValueError, parse_color, '#0ff00o')

