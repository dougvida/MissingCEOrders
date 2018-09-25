import logging
from easygui import *
from ManageOutputFiles import missing_file, errors_file
import Configuration.AppConfiguration


def show_results(app_cfg: Configuration.AppConfiguration, orders, errors, total_count):
    """
    write the orders and errors list to the dialog box
    :param app_cfg:
    :param orders:
    :param errors:
    :param total_count:
    :return:
    """

    logger = logging.getLogger(app_cfg.app_name)

    outdata = app_cfg.codebox_title + "\n\n"
    outdata += f"Number of missing orders found: {len(orders)}" + "\n"
    outdata += f"Number of errors found: {len(errors)}" + "\n"
    outdata += f"Number of orders searched: {total_count}"
    logger.error(outdata + "\n")

    orders_str = ''
    if len(orders) > 0:
        orders_str = app_cfg.MISSING_ORDERS_HEADER + '\n'
        idx_cnt = 1
        for idx, er in enumerate(orders):
            orders_str += str(er).replace("[", "").replace("]", "").replace("'", '').replace(", ", ",") + "\n"
            idx_cnt += 1

        if missing_file(app_cfg, orders_str):
            logger.error("Failed to write Missing orders file", exc_info=True)

    errors_str = ''
    if len(errors) > 0:
        # errors_str = '\n\n' + 'ERRORS' + '\n'
        errors_str = app_cfg.STARLIMS_ERROR_HEADER + '\n'
        idx_cnt = 1
        for idx, er in enumerate(errors):
            # str_dt = str(datetime.datetime(er[4]))
            str_dt = str(er[4]).replace('-', "/")
            # str_dt = datetime.datetime.strptime(er[4], "%Y-%m-%d %H:%M:%S")
            er[4] = str_dt[0:10]
            stmp2 = str(er).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            errors_str += stmp2.replace(", ", ",") + "\n"
            # errors_str += str(er).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'",
            # "").replace(", ", ",") + "\n"
            idx_cnt += 1
            logger.warning('\n' + errors_str)
        if errors_file(app_cfg, errors_str):
            logger.error("Failed to write errors orders file", exc_info=True)

    # show the information screen
    if len(orders_str) < 1:
        orders_str = "No missing orders found"

    if len(errors_str) < 1:
        errors_str = "No errors found"
    else:
        errors_str = '\n\n' + 'ERRORS -------------------' + '\n' + errors_str

    logger.warning(errors_str)

    codebox(outdata, app_cfg.codebox_title, orders_str + "\n" + errors_str)
