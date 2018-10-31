import os
from Utilities.FileUtility import folder_exists

APP_VERSION: str = "v1.0.5"

HL7ORDERS_FILE: str = 'HL7Order*.xlsx'
CEORDERS_FILE: str = 'CeOrders*.xls?'

DATA_FOLDER: str = "test_data"
DEFAULT_APP_PATH: str = os.getcwd()
DEFAULT_DATA_PATH: str = os.path.join(os.getcwd(), DATA_FOLDER)

APP_NAME = "MissingCEOrders"
LOG_FILENAME: str = f"{APP_NAME}.log"
LOG_FOLDER: str = "log"
DEFAULT_LOG_PATH = os.path.join(os.getcwd(), LOG_FOLDER)

LOGGING_MSG_FORMAT = '%(asctime)s,%(name)-12s,%(levelname)-8s,%(message)s'
LOGGING_DATE_FORMAT = '%Y%m%d %H:%M:%S'

DATA_OUT = "dataout"

# make the folder if not exists
folder_exists(DEFAULT_DATA_PATH, True)

# make the folder if not exists
folder_exists(DEFAULT_LOG_PATH, True)
