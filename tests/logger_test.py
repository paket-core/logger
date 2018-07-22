"""Tests for logger module"""
from unittest import TestCase

import util.logger


class TestLogger(TestCase):
    """Testing logger."""
    def test_output(self):
        """Try all levels"""
        logger_name = 'pkt.logger'
        pkt_logger = util.logger.logging.getLogger(logger_name)
        # pylint: disable=protected-access
        levels = util.logger.logging._levelToName
        # pylint: enable=protected-access
        for level in sorted(levels.keys()):
            level_name = levels[level]
            message = 'Testing - %s' % level_name
            try:
                logging_function = getattr(pkt_logger, level_name.lower())
                logging_function(message)
                with self.assertLogs(logger_name, level=level_name) as log_capture:
                    logging_function(message)
                    self.assertIn(message, log_capture.output[0])
            except AttributeError:
                pkt_logger.warning('No logging function for %s(%s)', level_name, level)
