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
