"""Test the package."""
import os.path
import sys

# Python imports are silly.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# pylint: disable=wrong-import-position
import logger
# pylint: enable=wrong-import-position

logger.setup()

LOGGER = logger.logging.getLogger('pkt.logger')

# pylint: disable=protected-access
for level in sorted(logger.logging._levelToName.keys()):
    LOGGER.log(level, "Testing - %s - %s%s", logger.logging._levelToName[level], sys.argv[0], sys.argv[1:])
