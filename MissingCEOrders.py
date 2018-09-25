"""
Missing CE Orders Applications

This is a simple script to search a HL7 file based on
user defined entries.   Segments, Field and field value
Application will prompt the user to select the HL7Order file
Application will prompt the user to sekect the CareEvolve file

***************************************
To docstring from the script
import pydocdir
import HL7Search
pydoc.help(HL7Search)
***************************************

Version 1.0.0 - first cut
Version 1.0.2 - Added DB search
Version 1.0.3 - Added AppConfiguration class
                Added -o and -p parameters

Easygui  http://easygui.sourceforge.net/tutorial.html#codebox
Make into an EXE
pip install pyinstaller
or
pip install --upgrade pyinstaller

pyinstaller --onefile <your_script_name>.py
# --onefile PyInstaller to create only one file. If you don’t
            specify this, the libraries will be distributed as
            separate file along with the executable.

python MissingCEOrders.py -s HL7Orders082218.xlsx -c CEOrders082318.xls -a 180415043
python MissingCEOrders.py -f <folder>
"""

from sys import exit, argv

import os
import json
import logging.config

import openpyxl
import xlrd
from easygui import msgbox, buttonbox

from Arguments import Arguments
from Configuration.AppConfiguration import *
from DB.DB_SyncMissingOrders import DBAccess, DBExceptions
from ShowResults import show_results
from Utilities.FileGUIUtility import getfile
from Utilities.General import is_number, fix_ce_order_number


#def setup_logging(
#        default_path='logging.json',
#        default_level=logging.INFO,
#        env_key='LOG_CFG'
#):
#    """Setup logging configuration
#
#    """
#    path = default_path
#    value = os.getenv(env_key, None)
#    if value:
#        path = value
#    if os.path.exists(path):
#        with open(path, 'rt') as f:
#            config = json.load(f)
#        logging.config.dictConfig(config)
#    else:
#        logging.basicConfig(level=default_level)

# def create_timed_rotationg_log(log_pathname):
#
#    # logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(message)s")
#    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                        datefmt='%m-%d %H:%M', filename='%(log_pathname)', filemode='w')
#
#    logger = logging.getLogger('__name__')
#    logger.setLevel(logging.INFO)
#
#    handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCounts=5)
#    logger.addHandler(handler)
# logging.basicConfig(filename="test.log", level=logging.DEBUG, format="%(asctime)s:%(message)s"
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M',
#                    filename='%(log_pathname)', filemode='w')


def process_files(sl_file, ce_file):
    """This script will the process the selected HL7 file.
    It search and provide feedback for based on the segment, field and data
    value requested

    :param sl_file: HL7 orders file extracted from StarLims
    :param ce_file: orders file exported from CareEvolve
    :return: N/A
    """

    # starlims_orders: List[(str, str, str, str)] = []
    # starlims_errors: List[(str, str, str, str, str, str)] = []

    # testing the date range class
    # date_range = DateRange()

    # If sl_file is None use the database to fetch orders
    # Remember the Orders table for STARLiMS is 1 to 2 hours behind
    if sl_file is None:
        logger.warning("Using database to access order data")
        try:
            mydbcls = DBAccess(config.username, config.password, -25)
            starlims_orders = mydbcls.fetch_non_errors()
            starlims_errors = mydbcls.fetch_errors()
            result = (starlims_orders, starlims_errors)

        except ValueError as err:
            stmp1 = f"Exception - process_files : {str(err)})"
            logger.exception(stmp1)
            raise DBExceptions(stmp1)
    else:
        # Process from the StarLims Excel file
        result = process_hl7_orders(sl_file)

    # check if file name ext is .xls or .xlsx
    if ce_file is None:
        logger.error("Error CE orders file was not selected")
        return

    name, ext = os.path.splitext(ce_file)
    if ext == '.xlsx':
        # newer excel file
        process_xlsx_file(ce_file, result[0], result[1])
    elif ext == '.xls':
        # old 2003 workbook
        process_xls_file(ce_file, result[0], result[1])
    else:
        logger.error(f"Error with source file.  Not correct file type: {ce_file}")

    return


def process_hl7_orders(filepathname):
    """ Process the Starlims HL7 order file or fetch HL7 orders from the DB.
    Add all valid entries in the order list
    Add any errors into the errors list
    If using the file format the file must be an Excel format: .xlsx
    :rtype: List: orders, List: errors
    :return: tuple(orders, errors)
    """

    orders: [(str, str, str, str)] = []
    errors: [(str, str, str, str, str, str)] = []

    # open and read StarLims HL7Orders file new format .xlsx
    wb = openpyxl.load_workbook(filename=filepathname, data_only=True)
    sheet = wb.active

    # read each row in the sheet
    for idx, row in enumerate(sheet.rows):
        if idx == 0:
            continue  # skip header

        hl7_order_id = str(row[0].value).strip().upper()
        order_status = str(row[3].value).strip()
        ce_order = str(row[4].value).strip()
        accession = str(row[5].value).strip()
        msg_id = row[1].value

        # msg_dt = datetime.datetime.strptime(msg_id, "%Y-%m-%d %H:%M:%S")
        # msg_date = datetime.datetime(msg_id, "%Y%m%d")
        msg_date = "{0:%Y/%m/%d}".format(msg_id)

        if order_status == 'Error' and accession == 'None':
            ack_by = str(row[7].value).strip()
            if ack_by == 'None':
                errors.append([hl7_order_id, ce_order, accession, order_status, msg_date,
                               'Review Error in Starlims-HL7 Orders tab - HL7ORD'])
            continue

        # add the entry to the list
        orders.append([hl7_order_id, ce_order, accession, order_status])

    # return both orders and errors lists
    return orders, errors


def process_xlsx_file(filepathname, orders, errors):
    """ Process the CareEvolve file after is has been converted to the new Excel
    format. Loop through this file for each order number searching for a match
    in the orders list

    :param filepathname: CEOrdersmmddyy.xlsx'
    :param orders: List
    :param errors: List
    :return: N/A
    """

    missing_orders: [[str, str, str]] = []
    total_entries = 0

    logger.info(f"Process_excel_file:  {filepathname}")
    # read the CE Orders Excel file
    try:
        wb = openpyxl.load_workbook(filename=filepathname, data_only=True)
        sheet = wb.active

        break_cnt = 0
        for idx, row in enumerate(sheet.rows):
            # skip all rows that don't have a order number
            if not str(row[6].value).isnumeric():
                continue

            status_add = ''
            total_entries += 1
            order_number = str(row[6].value).strip()
            order_date = str(row[8].value).strip()
            status = str(row[12].value).strip()
            created_by = str(row[14].value).strip().upper()

            if status != 'Complete':  # only want to look for completed orders
                continue

            # check if created by a demo user
            if created_by.__contains__('JANEDOE') or created_by.__contains__('JOHNDOE'):
                continue

            order_number = fix_ce_order_number(order_number)

            if any(order_number in s for s in orders):
                print('-', end='', flush=True)
            else:
                # not found
                print(r'X', end='', flush=True)
                # lets check if the order number is in the errors list
                if any(order_number in s for s in errors):
                    # yes found now lets get the HL7Order number and add to the output
                    for er1 in errors:
                        if er1[1] == order_number:
                            # we found it so lets add the HL7 Order number for easy lookup in StarLims
                            order_number = er1[0] + "," + order_number
                            status_add = ", " + er1[5]
                            break
                else:
                    order_number = "N/A," + order_number
                    status_add = " - Order not found in STARLims"

                missing_orders.append([order_number, order_date, str(status + status_add)])

            break_cnt += 1
            if break_cnt % 80 == 0:
                print(r'', flush=True)

    except openpyxl.utils.exceptions.InvalidFileException as err:
        logger.info(f'Exception: {err}')
        time_to_quit('Upgrade excel file to newer version', 'Open CE Order file')

    except IOError as ioe:
        time_to_quit('IO Error', f'Open CE Order file: {str(ioe)}')

    print(' ', flush=True)
    missing_orders.sort()

    show_results(app_cfg, missing_orders, errors, total_entries)


def process_xls_file(filenamepath, orders, errors):
    """ Process the CareEvolve file.  If directly it will be a 2003 workbook
    old Excel format.
    loop through this file searching for entries in the starlims_orders list

    :param filenamepath: CEOrdersmmddyy.xlsx'
    :param orders: List
    :param errors: List
    :return: None
    """

    missing_orders: [[str, str, str]] = []
    total_entries = 0

    logger.info(f"Process_excel_file: {filenamepath}")
    try:
        wb = xlrd.open_workbook(filename=filenamepath, on_demand=True)
        logger.info(f'WorkBook sheets: {wb.nsheets}')
        logger.info(f'WorkBook sheet names: {wb.sheet_names()}')
        p = wb.sheet_by_index(0)
        # p = wb.sheet_by_name(name='Sheet1')

        break_cnt = 0
        for row in p.get_rows():
            if row[6].value == '':
                continue
            if not is_number(row[6].value):
                continue

            total_entries += 1
            order_number = str(int(float(row[6].value))).strip()
            order_test = str(row[7].value).strip()
            order_date = str(row[8].value).strip()
            status = str(row[12].value).strip()
            created_by = str(row[14].value).strip().upper()

            # str_date = str(row[8].value).strip()
            # order_date2 = datetime.datetime.strptime(str_date, "%Y/%m/%d")

            # check if created by a demo user
            if created_by.__contains__('JANEDOE') or created_by.__contains__('JOHNDOE'):
                continue

            status_add = ''
            if len(order_test) <= 0:
                status_add = " - *** BAD order has no tests"

            # only want to look for completed orders
            if status != 'Complete':
                continue

            order_number = fix_ce_order_number(order_number)

            # found = 'None'
            # for cnt, row1 in enumerate(orders):
            #    if cnt % 80 == 0:
            #        print(r'', flush=True)
            #    if x2 != row1[2]:
            #        print('.', end='', flush=True)
            #        continue
            #    else:
            #        print(r'X', end='', flush=True)
            #        found = row1

            # if found == 'None':
            #    missing_orders.append([x2, order_date, status])

            if any(order_number in s for s in orders):
                print('-', end='', flush=True)
            else:
                # not found
                print(r'X', end='', flush=True)
                # lets check if the order number is in the errors list
                if any(order_number in s for s in errors):
                    # yes found now lets get the HL7Order number and add to the output
                    for er1 in errors:
                        if er1[1] == order_number:
                            # we found it so lets add the HL7 Order number for easy lookup in StarLims
                            order_number = er1[0] + "," + order_number
                            status_add = ", " + er1[5]
                            break
                else:
                    order_number = "N/A," + order_number
                    status_add = " - Order not found in STARLims"

                missing_orders.append([order_number, order_date, str(status + status_add)])

            break_cnt += 1
            if break_cnt % 80 == 0:
                print(r'', flush=True)

        print(' ', flush=True)
        if len(missing_orders) > 1:
            missing_orders.sort()

    except ValueError as ve:
        msgbox(title=app_cfg.codebox_title + f" - Exception:  Parsing file {filenamepath}",
               msg=f"{app_cfg.app_version} \n\nException {str(ve)} \n\n str{ValueError}\n\nFile may not be formatted"
                   f" correctly.\n\nOpen the file in Excel and save it to correct the issue.\n\nVerify contents are correct.")
        return

    show_results(app_cfg, missing_orders, errors, total_entries)


def time_to_quit(my_msg, str_title):
    """ Give the user a choich to Quit or Continue"""

    # msg = "Do you want to search again?"
    choices = ["Quit", "Continue"]
    reply = buttonbox(my_msg, title=str_title, choices=choices)
    if reply == "Quit":
        logger.warning("User selected Quit")
        return True
    else:
        return False


def msg(errstr1=''):
    """ Helper for additional usage message"""
    stmp1 = "Usage:\n" \
            "python MissingCEOrders.py (this will prompt the user for files\n" \
            "python MissingCEOrders.py -s <HL7OrdersFile> -c <CEOrdersFile> -a <accessionNumber>\n" \
            "                          no prompt will be given\n" \
            "python MissingCEOrders.py -a <accession> argument is used to search for a specific accession number\n" \
            "                          Prompt for CareEvolve file\n" \
            "python MissingCEOrders.py -s <hl7file> argument is the Starlims HL7 Orders files.  Export from HL7 Orders tab\n" \
            "                          Use this file as the master.  If blank will use the synced DB\n" \
            "python MissingCEOrders.py -c <cdfile> argument is the CareEvolve file created by exporting the \n" \
            "                             Audit reports=>Orders Created By report\n"

    if errstr1:
        stmp1 += f"\nError {errstr1}"

    return stmp1


if __name__ == "__main__":
    """ MissingCEOrders - This script has the ability to search from the 
    synced database of an excel file for HL7 orders from Starlims.   The 
    controlling method is if the user select a file or clicks on Cancel from 
    the first file dialog.   If a file is selected it than the file method 
    will be used.  If the user clicks on the Cancel button than the database 
    method will be used."""

    app_cfg = AppConfiguration(True)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # load the logging configuration
    logging.config.fileConfig('logging.ini')

    starlims_filename = app_cfg.hl7_orders_base_filename
    ce_filename = app_cfg.ce_orders_base_filename
    accession_number = 0
    stmp: str = ''

    my_args = Arguments()

    args_dict = {}
    if len(argv[1:]) > 0:
        args_dict = my_args.parse(argv[1:])
        if args_dict.get('err') > 0:
            msg(args_dict.get('errmsg'))
            exit(2)     # error with command line arguments

        # check if we need to use a different path
        stmp = args_dict.get('data_path')
        if stmp:
            stmp = os.path.join("", stmp)
            if not os.path.exists(stmp):
                os.makedirs(stmp)
            app_cfg.data_path = stmp
            logger.info(f"Using non default folder for data files: {stmp}")

        # check if argument is StarLims orders file
        stmp = args_dict.get('hl7orders')
        if stmp:
            tup = my_args.verify_file('hl7orders', app_cfg.data_path)
            if tup[0] > 1:
                msg(tup[1])
                logger.error(f"Failed to locate (hl7orders) file: {tup[1]}", exc_info=True)
                exit(3)  # error with file validation
            else:
                starlims_filename = stmp

        # check if argument is CareEvolve orders file
        stmp = args_dict.get('cdorders')
        if stmp:
            tup = my_args.verify_file('ceorders', app_cfg.data_path)
            if tup[0] > 1:
                msg(tup[1])
                logger.error(f"Failed to locate (ceorders) file: {tup[1]}, exc_info=True")
                exit(3)  # error with file validation
            else:
                ce_filename = stmp

        # check if we need to look for a specific specimen Id
        stmp = args_dict.get('accnum')
        if len(stmp) > 0:
            find_this_accession = stmp
            logger.info(f"Look for this accession number: {find_this_accession}")

    # get the data folder
    src_path = app_cfg.data_path

    if not os.path.exists(src_path):
        os.makedirs(src_path)

    # build up file path
    sl_filename_path = os.path.join(src_path, starlims_filename)
    ce_filename_path = os.path.join(src_path, ce_filename)

    # Add message box letting the user know to hit cancel for first select
    # file will use the DataBase
    msgbox(title=app_cfg.codebox_title + " - Note: Please read processing instructions",
           msg=f"{app_cfg.app_version} \n\n"
               "To use the database lookup: \n"
               "At the first file dialog click 'Cancel' \n"
               "To process via a file \n"
               "At the first file dialog select the file to process")

    sl_file_name_path: str = ''
    ce_file_name_path: str = ''
    errmsg: str = ''
    while True:
        # show File Dialog to select the master file
        logger.info(app_cfg.app_version)
        sl_file_name_path, errmsg = getfile(app_cfg.codebox_title, '', 'Please select the HL7 Order file to '
                                                                       'process', sl_filename_path)
        """        
        # if starlims_filenamepath is None:
            # we are using Database to get STARLiMS orders

            #if errmsg.lower() == 'file not found':
            #    if time_to_quit("File not found.  Do you want to Quit?", codebox_title):
            #        exit(-1)
            #    else:
            #        continue
            #if errmsg.lower() == 'Invalid file name':
            #    if time_to_quit("File selected is not an HL7 file. Do you want to Quit?", codebox_title):
            #        exit(-2)
            #    else:
            #        continue

            #if errmsg.lower() == 'cancel':
            #    if time_to_quit("No file selected. Do you want to Quit?", codebox_title):
            #        exit(-3)
            #    else:
            #        continue
        """

        # show File Dialog to select the CE white list file
        ce_file_name_path, err_msg = getfile(app_cfg.codebox_title, '', 'Please select the CE Order file to '
                                                                        'process', ce_filename_path)
        if ce_file_name_path is None:
            if errmsg.lower() == 'file not found':
                if time_to_quit("File not found.  Do you want to Quit?", app_cfg.codebox_title):
                    logger.error("Failed to locate (ceorders) file", exc_info=True)
                    exit(-1)
                else:
                    continue
            if errmsg.lower() == 'Invalid file name':
                if time_to_quit("File selected is invalid.  Do you want to Quit?", app_cfg.codebox_title):
                    logger.error("Invalid file name", exc_info=True)
                    exit(-2)
                else:
                    continue
            if errmsg.lower() == 'cancel':
                if time_to_quit("No file selected.  Do you want to Quit?", app_cfg.codebox_title):
                    logger.error("No file selected", exc_info=True)
                    exit(-3)
                else:
                    continue

        logger.warning(f"HL7Order file:{sl_file_name_path} - CEOrder file: {ce_file_name_path}")

        # go do the work
        if ce_file_name_path is None:
            logger.error("CE order file was not selected.  This is required", exc_info=True)
        else:
            try:
                process_files(sl_file_name_path, ce_file_name_path)
            except DBExceptions as dbe:
                logger.exception(f"DB Exception : {str(dbe)}", exc_info=True)
                exit(-1)

        # Prompt the user to search again?
        if time_to_quit("Want to search again?", app_cfg.codebox_title):
            exit(0)
