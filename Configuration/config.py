import os
from Utilities.FileUtility import folder_exists

APP_VERSION: str = "v1.0.3"
APP_CHG_HISTORY: str = "1.0.0 - Initial creation" + "\n" \
                       "1.0.1 - Added GUI" + "\n" \
                       "1.0.2 - Added Database search" + "\n" \
                       "1.0.3 - Added Logging" + "\n"

HL7ORDERS_FILE: str = 'HL7Order*.xlsx'
CEORDERS_FILE: str = 'CeOrders*.xls?'

DATA_FOLDER: str = "test_data"
DEFAULT_APP_PATH: str = os.getcwd()
DEFAULT_DATA_PATH: str = os.path.join(os.getcwd(), DATA_FOLDER)

APP_NAME = "MissingCEOrders"
LOG_FILENAME: str = f"{APP_NAME}.log"
LOG_FOLDER: str = "log"
DEFAULT_LOG_PATH = os.path.join(os.getcwd(), LOG_FOLDER)

# make the folder if not exists
folder_exists(DEFAULT_DATA_PATH, True)

# make the folder if not exists
folder_exists(DEFAULT_LOG_PATH, True)
