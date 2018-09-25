"""
Class for performing some date operations

"""
from datetime import datetime, timedelta


class DateRange:

    def __init__(self, days: int=-25):
        self._start_dt = None
        self._end_dt = None
        self.get_start_end_date_range_offset(days)

#    def get_start_dt_offset(self, days: int = -25):
#        """
#        Adjust the start date time back
#        days = 0 Start time will be today at 00:00:00.000Z and End time will be today at 23:59:59.999Z
#        days < 0 Start time is number of days backwards with time of 00:00:00.000Z and End time will be today at 23:59:59.999Z
#        days > 0 Same as if days = 0
#        :param int days:
#        :return Dict("start_dt", "end_dt":
#        """
#        today = datetime.today()
#
#        # in this format 'YYYY-MM-DD HH:MM:SS.sss'
#        self.end_dt = today.strftime('%Y-%m-%d T23:59:59.999Z')
#
#        # in this format 'YYYY-MM-DD HH:MM:SS.sss'
#        if days == 0:
#            # in this format 'YYYY-MM-DD HH:MM:SS.sssZ'
#            self.start_dt = today.strftime('%Y-%m-%d T00:00:00.000Z')
#        else:
#            self.start_dt = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d T00:00:00.000Z')
#
#        # print("DateRange: {}:{}".format(self.start_dt, self.end_dt))
#        return {"start_dt": self.start_dt, "end_dt": self.end_dt}

    def get_start_end_date_range_offset(self, days: int = 0):
        """
        Depending on the days_back value will determine the date time range.
        days = 0 Start time will be today at 00:00:00.000Z and End time will be today at 23:59:59.999Z
        days < 0 Start time is number of days backwards with time of 00:00:00.000Z and End time will be today at 23:59:59.999Z
        days > 0 Start time will be today at 00:00:00.000Z end time is number of days forward time of 23:59:59.999Z
        :param days:
        :return Dict("start_dt", "end_dt")
        """

        today = datetime.today()
        if days == 0:
            # in this format 'YYYY-MM-DD HH:MM:SS.sss'
            self._start_dt = today.strftime('%Y-%m-%d 00:00:00.000')

            # in this format 'YYYY-MM-DD HH:MM:SS.sss'
            self._end_dt = today.strftime('%Y-%m-%d 23:59:59.999')

        elif days < 0:
            self._start_dt = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d 00:00:00.000')

            # in this format 'YYYY-MM-DD HH:MM:SS.sss'
            self._end_dt = today.strftime('%Y-%m-%d 23:59:59.999')

        elif days > 0:
            # in this format 'YYYY-MM-DD HH:MM:SS.sss'
            self._start_dt = today.strftime('%Y-%m-%d 00:00:00.000')

            # adjust the end date keep start date today at YYYY-MM-DD HH:MM:SS.sss
            self._end_dt = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d 23:59:59.999')

        return {"start_dt": self.start_dt, "end_dt": self.end_dt}

    @property
    def start_dt(self):
        return self._start_dt

    @start_dt.setter
    def start_dt(self, value):
        self._start_dt = value

    @property
    def end_dt(self):
        return self._end_dt

    @end_dt.setter
    def end_dt(self, value):
        self._end_dt = value

    def __str__(self):
        print("DateRange: {} : {}".format(self.start_dt, self.end_dt))
