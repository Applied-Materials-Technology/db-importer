from enum import Enum
from dbimporter.logger import logger

class Jsonfile(Enum):
    FILE1 = "jsonpath/jsonfile1.json"
    FILE2 = "jsonpath/jsonfile2.json"
    BADDATA = "src/formatopts/baddatatest.json"
    TENSILEDATA = "src/formatopts/tensiledata.json"
    CRYOTENSILE = "src/formatopts/cryo_tensile.json"
    TEMPDATA = "src/formatopts/temp_data.json"
    HIGHTEMPTENSILE = "src/formatopts/hightemp_tensile.json"


def set_json(file_type):

    if file_type == None:
        logger.warning(f"file structure not set, defaulting to option baddata")
        filename = Jsonfile.BADDATA.value
    elif file_type == "one":
        logger.info(f"file structure type set to one")
        filename = Jsonfile.FILE1.value
    elif file_type == "two":
        logger.info(f"file structure type set to two")
        filename = Jsonfile.FILE2.value
    elif file_type == "baddata":
        logger.info(f"file structure type set to baddata")
        filename = Jsonfile.BADDATA.value
    elif file_type == "tensiledata":
        logger.info(f"file structure type set to tensiledata")
        filename = Jsonfile.TENSILEDATA.value
    elif file_type == "cryotensile":
        logger.info(f"file structure type set to cryotensile")
        filename = Jsonfile.CRYOTENSILE.value
    elif file_type == "tempdata":
        logger.info(f"file structure type set to tempdata")
        filename = Jsonfile.TEMPDATA.value
    elif file_type == "hightemptensile":
        logger.info(f"file structure type set to hightemptensile")
        filename = Jsonfile.HIGHTEMPTENSILE.value
    else:
        logger.warning(f"file structure could not be determined, defaulting to option BADDATA")
        filename = Jsonfile.BADDATA.value

    return filename