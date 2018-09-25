

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def fix_ce_order_number(ord_num):
    """ We need to build the CareEvolve order number so it will match what is
    int
    the list from the HL7 Orders list
    :param ord_num: raw number from CareEvolve
    :return: fixed up number 10 digit number starting with 'CE'
    """

    # we need to fix up the order string by left padding with 0
    # max of 10 characters
    # set the first two characters to 'CE'
    x1 = ord_num.rjust(10, '0')
    return "CE" + x1[2:]
