"""Tests for currency_conversions module."""
import unittest

import util.currency_conversions

class EuroToBulTest(unittest.TestCase):
    """Test conversion from euro cents to BUL stroops."""

    def euro_to_bul_test(self):
        """Test conversion from euro cents to BUL stroops."""
        price = 10
        euro_cents_amount = 100
        bul_stroops = util.currency_conversions.euro_cents_to_bul_stroops(
            euro_cents_amount, price)
        self.assertEqual(
            bul_stroops, 1000,
            "{} BUL stroops expected, {} got instead".format(1000, bul_stroops))
