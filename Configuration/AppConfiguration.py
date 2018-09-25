import os
import logging
from Configuration import config as config
import Utilities.FileUtility

APP_VERSION: str = "v1.0.3"
HL7ORDERS_FILE: str = 'HL7Order*.xlsx'
CEORDERS_FILE: str = 'CeOrders*.xls?'

DATA_FOLDER: str = "test_data"
DEFAULT_APP_PATH: str = r"C:\Precision\Workspace\Python\testing\MissingCEOrders"
DEFAULT_DATA_PATH: str = os.path.join(f"{DEFAULT_APP_PATH}", DATA_FOLDER)

APP_NAME = "MissingCEOrders"
LOG_FILENAME: str = f"{APP_NAME}.txt"
LOG_FOLDER: str = "log"
DEFAULT_LOG_PATH = os.path.join(DEFAULT_APP_PATH, LOG_FOLDER)


class AppConfiguration(object):

    _datapath: str
    STARLIMS_ERROR_HEADER = "HL7ORD, Specimen ID, Accession, Status, Date, Error"
    MISSING_ORDERS_HEADER = "HL7ORD, Specimen ID, Date, Status, Error"

    def __init__(self, default_path: bool = False):
        """
        initialize the class.   default_path True means to use default if False use current working directory + '\test_data'
        :param default_path:
        """

        # if __debug__:
        # assert len(config.username) < 1 or len(config.password) < 1

        self._appname: str = f"{APP_NAME}"
        self._script: str = f"{self._appname}.py"
        self._appversion: str = f"Script: {self._appname} - {APP_VERSION}"
        self._codebox_title: str = "Missing CE Orders in STARLims"
        self._hl7orders_base_filename: str = HL7ORDERS_FILE
        self._ceorders_base_filename: str = CEORDERS_FILE
        self._dbusername: str = config.username
        self._dbpassword: str = config.password
        self._datapath: str = ''
        if default_path is True:
            self.data_path = os.path.join("", DEFAULT_DATA_PATH)
            self._logfile_path = os.path.join("", DEFAULT_LOG_PATH)
            Utilities.FileUtility.folder_exists(self._logfile_path, True)
        else:
            self.data_path = os.path.join(os.getcwd(), DATA_FOLDER)
            self._logfile_path = os.path.join(os.getcwd(), LOG_FOLDER)
            Utilities.FileUtility.folder_exists(self._logfile_path, True)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M', filename='test.log', filemode='w')

    @property
    def app_name(self):
        return self._appname

    @property
    def app_script(self):
        return self._script

    @property
    def app_version(self):
        return self._appversion

    @property
    def codebox_title(self):
        return self._codebox_title

    @property
    def hl7_orders_base_filename(self):
        return self._hl7orders_base_filename

    @property
    def ce_orders_base_filename(self):
        return self._ceorders_base_filename

    @property
    def db_username(self):
        return self._dbusername

    @property
    def db_password(self):
        return self._dbpassword

    @property
    def data_path(self):
        return self._datapath

    @data_path.setter
    def data_path(self, value):
        if os.path.exists(value):
            self._datapath = value
        else:
            # does not exist.  Log error and set to default
            logging.error(f"path does not exist: {value}.  Set to use current working directory", exc_info=True)
            self._datapath = os.path.join(os.getcwd(), DATA_FOLDER)

    @property
    def log_name(self):
        return self._appname

    @property
    def logfile_path(self):
        return self._logfile_path

    @logfile_path.setter
    def logfile_path(self, value):
        if os.path.exists(value):
            self._logfile_path = value
        else:
            # does not exist.  Log error and set to default
            logging.error(f"path does not exist: {value}.  Set to use current working directory", exc_info=True)
            self._datapath = os.path.join(os.getcwd(), LOG_FOLDER)

    def __str__(self):
        return f"{self.app_name} > {self.__class__.__name__} : {self.ce_orders_base_filename}"

    def __repr__(self):
        return f"<{self.__class__.__name__}, {self.app_name} : {self.app_version}>"
