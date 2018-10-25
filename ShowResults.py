import logging
from Configuration import AppConfiguration
from Configuration import Config

from easygui import *
from ManageOutputFiles import missing_file, errors_file


def show_results(app_cfg: AppConfiguration, orders, errors, total_count):
    """
    write the orders and errors list to the dialog box
    :param app_cfg:
    :param orders:
    :param errors:
    :param total_count:
    :return:
    """

    orders_str: [str] = []
    ord_str: str = ''
    stmp = ''

    logger = logging.getLogger(app_cfg.app_name)

    outdata = '\n' + app_cfg.codebox_title + "\n\n"
    outdata += f"Number of missing orders found: {len(orders)}" + "\n"
    outdata += f"Number of errors found: {len(errors)}" + "\n"
    outdata += f"Number of orders searched: {total_count}"
    logger.error(outdata + "\n")

    if len(orders) > 0:
        logger.error("***** Missing orders ****")
        stmp = "***** Missing orders ****" + '\n' + app_cfg.MISSING_ORDERS_HEADER + '\n'
        orders_str.append(stmp)
        ord_str = stmp
        logger.error(app_cfg.MISSING_ORDERS_HEADER)
        idx_cnt = 1
        for idx, er in enumerate(orders):
            stmp = str(er).replace("[", "").replace("]", "").replace("'", '').replace(", ", ",")
            orders_str.append(stmp)
            ord_str += (stmp + '\n')
            logger.error(stmp)
            idx_cnt += 1

        if missing_file(app_cfg, orders_str):
            logger.error("Failed to write Missing orders file", exc_info=True)

    errors_str: [str] = []
    err_str: str = ''
    if len(errors) > 0:
        logger.error("***** Order Errors in STARLiMS ****")
        stmp = "***** Order Errors in STARLiMS ****" + '\n' + app_cfg.STARLIMS_ERROR_HEADER + '\n'
        errors_str.append(stmp)
        err_str = stmp
        logger.error(app_cfg.STARLIMS_ERROR_HEADER)
        idx_cnt = 1
        for idx, er in enumerate(errors):
            # str_dt = str(datetime.datetime(er[4]))
            str_dt = str(er[4]).replace('-', "/")
            # str_dt = datetime.datetime.strptime(er[4], "%Y-%m-%d %H:%M:%S")
            er[4] = str_dt[0:10]
            stmp2 = str(er).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            stmp = stmp2.replace(", ", ",")

            errors_str.append(stmp)
            err_str += (stmp + '\n')
            logger.error(stmp)
            idx_cnt += 1

        if errors_file(app_cfg, errors_str):
            logger.error("Failed to write errors orders file", exc_info=True)

    # show the information screen
    if len(orders_str) < 1:
        logger.warning("No missing orders found")

    if len(errors_str) < 1:
        logger.warning("No errors found")

    codebox(outdata, app_cfg.codebox_title, ord_str + "\n" + err_str)

    logger.info('\n')

