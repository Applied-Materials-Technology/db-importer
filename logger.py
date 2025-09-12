import logging
import sys
import logging.handlers


logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

#file_handler = logging.FileHandler('issues.log')
file_handler = logging.handlers.RotatingFileHandler("example.log", mode = 'w', backupCount = 5)

console_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

"""
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
logger.exception('An exception')"""