"""Tests for countly module"""
import unittest

import util.countly
import util.logger


class TestCountly(unittest.TestCase):
    """Tests for sending countly events"""

    def test_countly(self):
        """Test countly availability"""
        key = 'test_event'
        count = 5
        with self.assertLogs('pkt.util', level=util.logger.logging.DEBUG) as log_capture:
            util.countly.send_countly_event(key, count)
            # we have 3 logger outputs on success request
            self.assertEqual(len(log_capture.output), 3)
            self.assertIn('{"result":"Success"}', log_capture.output[2])

    def test_invalid_parameters(self):
        """Test send_countly_event behavior on invalid args"""
        data_set = [
            {
                'key': 456.78,  # invalid key
                'count': 5,
                'begin_session': 123456789,
                'end_session': 133456798
            },
            {
                'key': 'test_event',
                'count': 'five',  # invalid count
                'begin_session': 123456789,
                'end_session': 133456798
            },
            {
                'key': 'test_event',
                'count': 5,
                'begin_session': 'qwerty',  # invalid begin_session
                'end_session': 123456789
            },
            {
                'key': 'test_event',
                'count': 5,
                'begin_session': 123456789,
                'end_session': 'qwerty'  # invalid end_session
            }
        ]
        for args in data_set:
            with self.subTest(**args):
                self.assertRaises(ValueError, util.countly.send_countly_event, **args)
