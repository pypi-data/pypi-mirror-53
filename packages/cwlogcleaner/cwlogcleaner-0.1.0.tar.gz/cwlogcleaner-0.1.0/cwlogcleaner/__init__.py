import logging
import sys

__version__ = '0.1.0'

logger = logging.getLogger('cwlogcleaner')
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
