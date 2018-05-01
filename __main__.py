import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# pylint: disable=wrong-import-position
# Python imports are silly.
import logger

# pylint: enable=wrong-import-position

logger.setup()

LOGGER = logger.logging.getLogger('pkt.logger')

if __name__ == '__main__':
    LOGGER.debug("a debug message")
    LOGGER.info("an info message")
    LOGGER.warning("a warning message")
    LOGGER.error("an error message")
