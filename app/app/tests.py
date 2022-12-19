"""
Sample Tests
"""

from django.test import SimpleTestCase

from .calc import add


class CalcTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        res = add(5, 6)
        self.assertEqual(res, 11)
