import sys
from unittest import TestCase

import logger


class TestLogger(TestCase):
    def test_output(self):
        logger.setup()
        logger_name = 'pkt.logger'
        pkt_logger = logger.logging.getLogger(logger_name)
        for level in sorted(list(logger.logging._levelToName.keys())[1:]):
            level_name = logger.logging._levelToName[level]
            with self.assertLogs(logger_name, level=level_name) as cm:
                message = 'Testing - %s - %s%s' % (level_name, sys.argv[0], sys.argv[1:])
                pkt_logger.log(level, message)
                self.assertIn(message,  cm.output[0])
