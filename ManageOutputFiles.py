import os
from datetime import datetime
from Utilities.FileUtility import write_file
import logging

logger = logging.getLogger('MissingCEOrders')


def errors_file(app_cfg, datastr):
    """
    write the errors data to the errors file
    :param app_cfg: app configuration object
    :param datastr:
    :param logger:
    :return: True = failure; False = successful
    """
    error: bool = False
    try:
        # get the date as yyyymmdd
        filename = "OrderErrors_" + datetime.now().strftime("%Y%m%d") + ".csv"
        file_cwd = os.path.join(app_cfg.get_data_path(), app_cfg.DATA_OUTPUT)
        if not os.path.exists(file_cwd):
            os.makedirs(file_cwd)

        filepathname = file_cwd + os.path.join("\\", filename)
        write_file(filepathname, datastr)

    except ValueError as ve:
        logging.warning(f"Exception writing errors file {filename} - print({ve})")
        error = True

    finally:
        return error


def missing_file(app_cfg, datastr):
    """
    write the missing orders to the missingCE file
    :param app_cfg: app configuration object
    :param datastr:
    :param logger:
    :return: True = failure; False = successful
    """

    error: bool = False
    try:
        # get the date as yyyymmdd
        filename = "MissingCEOrders_" + datetime.now().strftime("%Y%m%d") + ".csv"
        # file_cwd = os.getcwd() + os.path.join("", "\\") + os.path.join("", filename)
        file_cwd = os.path.join(app_cfg.get_data_path(), app_cfg.DATA_OUTPUT)
        if not os.path.exists(file_cwd):
            os.makedirs(file_cwd)

        filepathname = file_cwd + os.path.join("\\", filename)
        write_file(filepathname, datastr)

    except ValueError as ve:
        logging.warning(f"Exception writing errors file {filename} - print({ve})")
        error = True

    finally:
        return error
