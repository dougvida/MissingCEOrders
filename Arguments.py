import os
import getopt
import logging


class Arguments:

    logger = logging.getLogger("MissingCEOrders")

    def __init__(self):
        self.argdict: dict = {}

    def parse(self, argv):
        """
        parse the arguments and map to the correct field is correct argument
        note: no arguments is allowed
        -a <accession> argument is used to search for a specific accession number
        -s <hl7file> argument is the Starlims HL7 Orders files.  Export from HL7 Orders tab
                     If no argument than script will use the Synced DB
        -c <cdfile> argument is the CareEvolve file created by exporting the Audit reports=>Orders Created By report"
        -o system leve __debug__ option
        -f <data folder> If present use this folder else use the current working folder + '\test_data'
        :type argv: object
        """

        # Rules:
        # if -s must have -c
        # if -c no -s will use the DB
        # if -s only error
        #
        # if -a with -s only search this file
        # if -a with -c only search this file
        # if -a with -s and -c search both files
        # if -a only search the DB

        st_file: str = ''
        ce_file: str = ''
        acc_num: str = ''
        err: int = 0
        errmsg: str = ''
        data_path: str = ''

        try:
            opts, args = getopt.getopt(argv, 's:c:a:f:ho', ['hl7file=', 'cefile=', 'accession=', 'data_path', 'help', 'debug'])
        except getopt.GetoptError as exp:
            # msg()
            logging.exception(f"{str(exp)}")

            return -1    # exception display error message and abort app

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                err = 1  # help prompt - display the help/usage message
                break
            elif opt in ('-s', '--hl7file'):
                st_file = arg
            elif opt in ('-c', '--cefile'):
                ce_file = arg
            elif opt in ('-a', '--accession'):
                acc_num = arg
            elif opt in ('-f', '--data_path'):
                if len(arg) > 4:
                    data_path = os.path.join("", arg)
            elif opt in ('-o', '--debug'):
                continue
            else:
                err = 2  # argument does not match
                errmsg = str(opt+", "+arg)
                break

        self.argdict = {'hl7orders': st_file, 'ceorders': ce_file, 'accnum': acc_num, 'err': err, 'errmsg': errmsg,
                        'data_path': data_path}
        return self.argdict

        # Rules:
        # if -s must have -c
        # if -c no -s will use the DB
        # if -s only error
        #
        # if -a with -s only search this file
        # if -a with -c only search this file
        # if -a with -s and -c search both files
        # if -a only search the DB

    @property
    def accession(self):
        return self.argdict.keys('accnum')

    @property
    def error(self):
        return self.argdict.keys('err')

    @property
    def hl7orders_file(self):
        return self.argdict.keys('hl7orders')

    @property
    def ceorders_file(self):
        return self.argdict.keys('ceorders')

    def verify_file(self, lookup_key: str, srcpath: str):
        """
        verify the file exists based on the dictionary Key value
        if the file does not exist than return False
        if the lookup key is invalid return False
        :param self:
        :param lookup_key:
        :param srcpath:
        :return tuple(int, str)
                int:  0 no error; 1 no key to search for; 2 Key does not exists; 3 file is invalid; 4 file does not exists
        """

        n_err: int = 0
        errmsg = ''

        if len(lookup_key) > 0:
            if lookup_key in self.argdict.keys():
                orders_file = self.argdict.get(lookup_key)
                # verify any file exists
                if len(orders_file) > 0:
                    if os.path.isfile(os.path.join(srcpath, orders_file)):
                        n_err = 0
                    else:
                        n_err = 4
                        errmsg = f"File '{orders_file}' does not exist at this location '{srcpath}'"
                else:
                    n_err = 3
                    errmsg = f"File is invalid: '{orders_file}'"
            else:
                n_err = 2
                errmsg = f"The key '{lookup_key}' not found in argument dictionary"
        else:
            n_err = 1
            errmsg = 'No lookup key provided'

        if n_err:
            logging.error(errmsg)

        return n_err, errmsg

    def verify_files(self, srcpath):
        """
        verify the file exists based on the dictionary Key value
        if the file does not exist than return False
        if the lookup key is invalid return False
        :param self:
        :param srcpath:
        :return tuple(int, str)
                int:  0 no error; 1 no key to search for; 2 Key does not exists; 3 file is invalid; 4 file does not exists
        """
        tup: tuple = ([0, ""])

        tup = self.verify_file('hl7orders', srcpath)
        if tup[0] > 1:
            # we have an error
            return tup

        tup = self.verify_file('ceorders', srcpath)
        if tup[0] > 1:
            # we have an error
            return tup

        return tup
