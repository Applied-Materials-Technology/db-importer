import logging
import logging.handlers
import sys

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.RotatingFileHandler("example.log", mode = 'w', backupCount = 5)

console_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def change_logging_level(console, outputfile):
    console_handler.setLevel(console)
    file_handler.setLevel(outputfile)


