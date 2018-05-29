"""Test the package."""
import sys

import logger

LOGGER = logger.logging.getLogger('pkt.logger')

logger.setup()

# pylint: disable=protected-access
for level in sorted(logger.logging._levelToName.keys()):
    LOGGER.log(level, "logger message - %s - %s", logger.logging._levelToName[level], sys.argv[1:])
