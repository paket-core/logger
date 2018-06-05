"""Tests for stellar units conversion"""
import unittest

import util.stellar_units


class TestStroopsToUnits(unittest.TestCase):
    """Tests for stroops_to_units function"""

    def test_valid_values(self):
        """Testing stroops_to_units function on valid data set"""
        data_set = {
            1: '0.0000001',
            10: '0.0000010',
            1234567: '0.1234567',
            5600: '0.0005600',
            1745127942: '174.5127942',
            1873987431248795178: '187398743124.8795178'
        }
        for input_value, expected_value in data_set.items():
            with self.subTest(input_value=input_value, expected_value=expected_value):
                output_value = util.stellar_units.stroops_to_units(input_value)
                self.assertEqual(output_value, expected_value)

    def test_numeric_representation(self):
        """Testing stroops_to_units function on valid data set with given numeric_representation option"""
        data_set = {
            1: 0.0000001,
            10: 0.000001,
            1234567: 0.1234567,
            5600: 0.00056,
            1745127942: 174.5127942,
            1873987431248795178: 187398743124.8795178
        }
        for input_value, expected_value in data_set.items():
            with self.subTest(input_value=input_value, expected_value=expected_value):
                output_value = util.stellar_units.stroops_to_units(input_value, numeric_representation=True)
                self.assertEqual(output_value, expected_value)

    def test_invalid_type(self):
        """Testing stroops_to_units function on data set of invalid type values"""
        data_set = [
            '456',
            10.458,
            True,
            [2789],
            {'value': 17}
        ]
        for invalid_type_value in data_set:
            with self.subTest(value=invalid_type_value):
                self.assertRaises(TypeError, util.stellar_units.stroops_to_units, invalid_type_value)


class TestUnitsToStroops(unittest.TestCase):
    """Tests for units_to_stroops function"""

    def test_valid_values(self):
        """Testing units_to_stroops function on valid data set"""
        data_set = {
            '0.0000001': '1',
            '0.000001': '10',
            '0.1234567': '1234567',
            '0.0005600': '5600',
            '174.5127942': '1745127942',
            '187398743124.8795178': '1873987431248795178'
        }
        for input_value, expected_value in data_set.items():
            with self.subTest(input_value=input_value, expected_value=expected_value):
                output_value = util.stellar_units.units_to_stroops(input_value)
                self.assertEqual(output_value, expected_value)

    def test_numeric_representation(self):
        """Testing units_to_stroops function on valid data set with given numeric_representation option"""
        data_set = {
            '0.0000001': 1,
            '0.000001': 10,
            '0.1234567': 1234567,
            '0.0005600': 5600,
            '174.5127942': 1745127942,
            '187398743124.8795178': 1873987431248795178
        }
        for input_value, expected_value in data_set.items():
            with self.subTest(input_value=input_value, expected_value=expected_value):
                output_value = util.stellar_units.units_to_stroops(input_value, numeric_representation=True)
                self.assertEqual(output_value, expected_value)

    def test_invalid_type(self):
        """Testing units_to_stroops function on data set of invalid type values"""
        data_set = [
            456,
            True,
            [2789],
            {'value': 17}
        ]
        for invalid_type_value in data_set:
            with self.subTest(value=invalid_type_value):
                self.assertRaises(TypeError, util.stellar_units.units_to_stroops, invalid_type_value)
