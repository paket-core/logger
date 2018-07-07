"""Tests for currencies conversion"""
import unittest

import util.conversion


class TestBaseConversion(unittest.TestCase):
    """Base class for all conversion tests"""

    def conversion(self, data_set, conversion_function, numeric_representation=False, message=None):
        """
        Make conversion on given data set with given conversion function
        :param dict data_set: Key-value set where keys is input data and values is expected result
        :param callable conversion_function: Function that makes conversion from one units to another
        :param bool numeric_representation: if true, result will be returned in numeric type (int or float)
        :param str message: Message to display in case of test failure
        """
        for input_value, expected_value in data_set.items():
            output_value = conversion_function(input_value, numeric_representation)
            with self.subTest(input_value=input_value, output_value=output_value, expected_value=expected_value):
                self.assertEqual(output_value, expected_value, message)


class TestInvalidTypes(TestBaseConversion):
    """Test conversion functions on invalid type arguments"""

    def test_invalid(self):
        """Test conversion functions on invalid type arguments"""
        data_set = [
            78.45,
            True,
            [2789],
            {'value': 17}
        ]
        conversion_functions = [
            util.conversion.btc_to_satoshi,
            util.conversion.satoshi_to_btc,
            util.conversion.eth_to_wei,
            util.conversion.wei_to_eth,
            util.conversion.units_to_stroops,
            util.conversion.units_to_stroops
        ]
        for invalid_type_value in data_set:
            for conversion_function in conversion_functions:
                with self.subTest(value=invalid_type_value, function=conversion_function.__name__):
                    self.assertRaises(TypeError, conversion_function, invalid_type_value,
                                      'TypeError was not raised on invalid type argument')


class TestBtcConversion(TestBaseConversion):
    """Test btc conversion"""

    def test_btc_to_satoshi(self):
        """Test btc to satoshi conversion"""
        data_set = {
            '10.0': '1000000000',
            '19.76516789': '1976516789',
            '7067.00079404': '706700079404',
            '10.00000001': '1000000001',
            '0.00000001': '1',
            123: '12300000000',
            1: '100000000',
            0: '0'
        }
        self.conversion(data_set, util.conversion.btc_to_satoshi, message='btc to satoshi conversion failed')

    def test_satoshi_to_btc(self):
        """Test satoshi to btc conversion"""
        data_set = {
            '1000000000': '10.0',
            '1000000001': '10.00000001',
            '12300000000': '123.0',
            '100000000': '1.0',
            '1': '0.00000001',
            '0': '0.0',
            '1403': '0.00001403',
            '8500': '0.000085',
            '10295000000': '102.95'
        }
        self.conversion(data_set, util.conversion.satoshi_to_btc, message='satoshi to btc conversion failed')

    def test_numeric_representation(self):
        """Test numeric representation of converted values"""
        test_sets = [
            {
                'name': util.conversion.btc_to_satoshi.__name__,
                'conversion_function': util.conversion.btc_to_satoshi,
                'data_set': {
                    '10.0': 1000000000,
                    '19.76516789': 1976516789,
                    '7067.00079404': 706700079404,
                    '10.00000001': 1000000001,
                    '0.00000001': 1,
                    123: 12300000000,
                    1: 100000000,
                    0: 0
                }
            },
            {
                'name': util.conversion.satoshi_to_btc.__name__,
                'conversion_function': util.conversion.satoshi_to_btc,
                'data_set': {
                    '1000000000': 10.0,
                    '1000000001': 10.00000001,
                    '12300000000': 123.0,
                    '100000000': 1.0,
                    '1': 0.00000001,
                    '0': 0.0,
                    '1403': 0.00001403,
                    '8500': 0.000085,
                    '10295000000': 102.95
                }
            }
        ]
        for test_set in test_sets:
            with self.subTest(conversion_name=test_set['name']):
                self.conversion(test_set['data_set'], test_set['conversion_function'], numeric_representation=True,
                                message='conversion function does not return expected numeric result')


class TestEthConversion(TestBaseConversion):
    """Test eth conversion"""

    def test_eth_to_wei(self):
        """Test eth to wei conversion"""
        data_set = {
            '10.0': '10000000000000000000',
            '19.76516789': '19765167890000000000',
            '7067.00079404': '7067000794040000000000',
            '10.00000004': '10000000040000000000',
            '0.00000001': '10000000000',
            '0.000000000000000009': '9',
            123: '123000000000000000000',
            1: '1000000000000000000',
            0: '0',
        }
        self.conversion(data_set, util.conversion.eth_to_wei, message='eth to wei conversion failed')

    def test_wei_to_eth(self):
        """Test wei to eth conversion"""
        data_set = {
            '10000000000000000000': '10.0',
            '10000000010000000000': '10.00000001',
            '123000000000000000000': '123.0',
            '100000000': '0.0000000001',
            '1': '0.000000000000000001',
            '0': '0.0',
            '1403': '0.000000000000001403',
            '8500': '0.0000000000000085',
            '10295000000': '0.000000010295'
        }
        self.conversion(data_set, util.conversion.wei_to_eth, message='wei to eth conversion failed')

    def test_numeric_representation(self):
        """Test numeric representation of converted values"""
        test_sets = [
            {
                'name': util.conversion.eth_to_wei.__name__,
                'conversion_function': util.conversion.eth_to_wei,
                'data_set': {
                    '10.0': 10000000000000000000,
                    '19.76516789': 19765167890000000000,
                    '7067.00079404': 7067000794040000000000,
                    '10.00000004': 10000000040000000000,
                    '0.00000001': 10000000000,
                    '0.000000000000000009': 9,
                    123: 123000000000000000000,
                    1: 1000000000000000000,
                    0: 0,
                }
            },
            {
                'name': util.conversion.wei_to_eth.__name__,
                'conversion_function': util.conversion.wei_to_eth,
                'data_set': {
                    '10000000000000000000': 10.0,
                    '10000000010000000000': 10.00000001,
                    '123000000000000000000': 123.0,
                    '1': 0.000000000000000001,
                    '0': 0.0,
                    '1403': 0.000000000000001403,
                    '10295000000': 0.000000010295
                }
            }
        ]
        for test_set in test_sets:
            with self.subTest(conversion_name=test_set['name']):
                self.conversion(test_set['data_set'], test_set['conversion_function'], numeric_representation=True,
                                message='conversion function does not return expected numeric result')


class TestStellarConversion(TestBaseConversion):
    """Test stellar units conversion"""

    def test_units_to_stroops(self):
        """Test stellar units to stroops conversion"""
        data_set = {
            '0.0000001': '1',
            '0.000001': '10',
            '0.1234567': '1234567',
            '0.0005600': '5600',
            '45': '450000000',
            '174.5127942': '1745127942',
            '1792.0045': '17920045000',
            '187398743124.8795178': '1873987431248795178',
            '1792.0045126789125479': '17920045126',
        }
        self.conversion(data_set, util.conversion.units_to_stroops,
                        message='stellar units to stroops conversion failed')

    def test_stroops_to_units(self):
        """Test stroops to stellar units conversion"""
        data_set = {
            1: '0.0000001',
            '1': '0.0000001',
            10: '0.000001',
            '10': '0.000001',
            1234567: '0.1234567',
            '1234567': '0.1234567',
            5600: '0.00056',
            '5600': '0.00056',
            50000000: '5.0',
            '50000000': '5.0',
            1745127942: '174.5127942',
            '1745127942': '174.5127942',
            1873987431248795178: '187398743124.8795178',
            '1873987431248795178': '187398743124.8795178'
        }
        self.conversion(data_set, util.conversion.stroops_to_units,
                        message='stroops to stellar units conversion failed')

    def test_numeric_representation(self):
        """Test numeric representation of converted values"""
        test_sets = [
            {
                'name': util.conversion.units_to_stroops.__name__,
                'conversion_function': util.conversion.units_to_stroops,
                'data_set': {
                    '0.0000001': 1,
                    '0.000001': 10,
                    '0.1234567': 1234567,
                    '0.0005600': 5600,
                    '45': 450000000,
                    '174.5127942': 1745127942,
                    '1792.0045': 17920045000,
                    '187398743124.8795178': 1873987431248795178,
                    '1792.0045126789125479': 17920045126,
                }
            },
            {
                'name': util.conversion.stroops_to_units.__name__,
                'conversion_function': util.conversion.stroops_to_units,
                'data_set': {
                    1: 0.0000001,
                    '1': 0.0000001,
                    10: 0.0000010,
                    '10': 0.0000010,
                    1234567: 0.1234567,
                    '1234567': 0.1234567,
                    5600: 0.0005600,
                    '5600': 0.0005600,
                    1745127942: 174.5127942,
                    '1745127942': 174.5127942,
                    1873987431248795178: 187398743124.8795178,
                    '1873987431248795178': 187398743124.8795178
                }
            }
        ]
        for test_set in test_sets:
            with self.subTest(conversion_name=test_set['name']):
                self.conversion(test_set['data_set'], test_set['conversion_function'], numeric_representation=True,
                                message='conversion function does not return expected numeric result')
