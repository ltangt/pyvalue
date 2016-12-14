# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD


class MorningStarFinancial(object):
    _stock = ""
    _revenue_in_millions = {}  # the key is the date and the value is the revenue in millions

    def __init__(self, stock, revenue = {}):
        self._stock = stock
        self._revenue_in_millions = revenue
        return

    @property
    def stock(self):
        return self._stock

    @property
    def revenue_in_millions(self):
        return self._revenue_in_millions

    @revenue_in_millions.setter
    def revenue_in_millions(self, revenue):
        self._revenue_in_millions = revenue

    def debug_info(self):
        info = self._stock
        info += " : "
        info += str(self._revenue_in_millions)
        return info

