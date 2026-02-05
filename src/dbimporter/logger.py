import logging
import logging.handlers
from dbimporter.printing import bcolours, Printer

printer = Printer()

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.RotatingFileHandler(f"{__name__}example.log", mode = 'w', backupCount = 5)

console_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class CustomFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord):

        start_style = {
            'DEBUG': bcolours.DEFAULT,
            'INFO': bcolours.INFO,
            'WARNING': bcolours.WARNING,
            'ERROR': bcolours.ERROR,
            'CRITICAL': bcolours.CRITICAL+bcolours.BOLD,
        }.get(record.levelname, bcolours.ENDC)

        end_style = bcolours.ENDC
        return printer.colour_logs(super().format(record), start_style)


formatter = CustomFormatter(format)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def change_logging_level(console, outputfile):

    """
    Change the logging level to that specified when making Check
    object
    """

    console_handler.setLevel(console)
    file_handler.setLevel(outputfile)


def set_log_formatter():

    """
    Reverts formatter with coloured logs to default colours
    if no_log_colour is True in Check object
    """

    formatter = logging.Formatter(format)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
