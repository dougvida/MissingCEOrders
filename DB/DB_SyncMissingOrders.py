from typing import List
import pyodbc

from DB.DBException import DBExceptions
from Utilities.DateRange import DateRange
from Configuration import AppConfiguration, Config, PW
import logging


class DBAccess:

    def __init__(self, start_dt_offset=-25):

        self.logging = None

        dtr = DateRange(start_dt_offset)
        self._start_dt = dtr.start_dt
        self._ent_dt = dtr.end_dt

        self._query_str = "SELECT HL7ORD, ORDERFILLERNUMBER as SPECIMEN_ID," \
                          "EXTERNAL_ID As ACCESSION, STATUS," \
                          "PRELOG_DATE As DATE, ERROR_MESSAGE" \
                          " FROM [dbo].[starlims_HL7_ORDERS_REVIEW] "

        # ''%Y-%m-%d T00:00:00.000Z''
        # " AND PRELOG_DATE >= '2018-07-01 00:00:00.000'"
        self._prelog_date = f" AND PRELOG_DATE >= '{self._start_dt}'"

        self._where_err = " WHERE (STATUS <> 'Done'" \
                          " AND ERROR_MESSAGE NOT like '%already present in the system')" \
                          " AND ACKNOWLEDGED_BY IS NULL" \
                          " AND ORDERFILLERNUMBER NOT like 'TEST%'" \
                          " AND ORDERFILLERNUMBER NOT like 'EMRT%'" \

        self._where_all = " WHERE ORDERFILLERNUMBER NOT like 'TEST%'" \
                          " AND ORDERFILLERNUMBER NOT like 'EMRT%'"

        self._where_non_errors = " WHERE STATUS = 'Done'" \
                                 " AND ORDERFILLERNUMBER NOT like 'TEST%'" \
                                 " AND ORDERFILLERNUMBER NOT like 'EMRT%'"

        self._order_by = " ORDER BY SPECIMEN_ID DESC, HL7ORD DESC, PRELOG_DATE"

        self._hl7_orders: List[(str, str, str, str)] = ["HL7ORD, SPECIMEN_ID, ACCESSION, STATUS, "
                                                        "DATE, ERROR_MESSAGE"]

        # setup the DB parameters
        self._server = 'pdx-dw-prod-srvr.database.windows.net'
        self._database = 'pdx-dw-prod'
        self._username = PW.username
        self._password = PW.password
        self._driver = '{ODBC Driver 13 for SQL Server}'

        self.cont_str = f"DRIVER={self._driver}; PORT=1433; DATABASE={self._database}; " \
                        f"SERVER={self._server}; UID={self._username}; PWD={self._password};"

        self._logging = logging.getLogger(Config.APP_NAME)

    def db_user_pwd(self, usr='', pwd=''):
        update = False
        if len(usr) > 1:
            self._username = usr
            update = True
        if len(pwd) > 1:
            update = True
            self._password = pwd

        if update:
            self.cont_str = f"DRIVER={self._driver}; PORT=1433; DATABASE={self._database}; " \
                            f"SERVER={self._server}; UID={self._username}; PWD={self._password};"

    def fetch_all(self):
        results = []

        foo = "DBAccess::fetch_all"

        # build the query string
        query = self._query_str + self._where_all + self._prelog_date + self._order_by
        stmp = f"{foo} - Query: {query}"
        self._logging.debug(stmp)
        results = self.fetch_data(query)

        if results is not None:
            stmp = f"{foo} - Number of rows returned: {len(results)}"
        else:
            stmp = f"{foo} - No results found"

        self._logging.info(stmp)
        return results

    def fetch_non_errors(self):
        results = []

        foo = "DBAccess::fetch_non_errors"

        # build the query string
        query = self._query_str + self._where_non_errors + self._prelog_date + self._order_by
        stmp = f"{foo} - Query: {query}"
        self._logging.debug(stmp)
        results = self.fetch_data(query)

        if results is not None:
            stmp = f"{foo} - Number of rows returned: {len(results)}"
        else:
            stmp = f"{foo} - No results found"

        self._logging.info(stmp)
        return results

    def fetch_errors(self):
        results = []

        foo = "DBAccess::fetch_errors"
        
        try:
            # build the query string
            query = self._query_str + self._where_err + self._prelog_date + self._order_by
            stmp = f"{foo} - Query: {query}"
            self._logging.debug(stmp)
            results = self.fetch_data(query)
            return results

        except pyodbc.ProgrammingError as sqlerr:
            # show the error
            stmp = f"***** SQL error: {foo} - {print(sqlerr)}"
            self._logging.error(stmp)
            results = None

        finally:
            stmp = f"{foo} - Number of rows returned: {len(results)}"
            self._logging.info(stmp)

    def fetch_data(self, query):
        results = []

        foo = "DBAccess::fetch_data"

        try:
            # execute the query
            with pyodbc.connect(self.cont_str) as cnxn:
                cursor = cnxn.cursor().execute(query)
                stmp = f"{foo} - Database connection successful - Performing data fetch"
                self._logging.info(stmp)

                # get all the rows found
                for row in cursor.fetchall():
                    results.append(row)

            return results

        except Exception as exp:
            stmp = f"***** EXCEPTION - {foo} - print{exp}"
            self._logging.exception(stmp)
            raise DBExceptions().my_exception(stmp)

        except pyodbc.DatabaseError as dbe:
            stmp = f"***** EXCEPTION - {foo} - {str(dbe)}"
            self._logging.exception(stmp)
            raise DBExceptions().my_exception(stmp)

        except pyodbc.ProgrammingError as sqlerr:
            stmp = f"***** EXCEPTION - {foo} - {str(sqlerr)}"
            self._logging.exception(stmp)
            raise DBExceptions().my_exception(stmp)
