# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import logging

logger = logging.getLogger('logging_tutorial')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

logger.debug('this is debug message')
logger.info('this is info message')
logger.warning('this is warning message')
logger.error('this is error message')
logger.critical('this is critical message')
