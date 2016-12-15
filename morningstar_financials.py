# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD


class MorningStarFinancial(object):
    _stock = ""
    _revenue_in_millions = {}  # the key is the date and the value is the revenue in millions
    _net_income_in_millions = {}  # the key is the date and the value is the net income in millions
    _book_value_per_share = {} # the key is the date and the value is the book value per share

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

    @property
    def net_income_in_millions(self):
        return self._net_income_in_millions

    @net_income_in_millions.setter
    def net_income_in_millions(self, net_income):
        self._net_income_in_millions = net_income

    @property
    def book_value_per_share(self):
        return self._book_value_per_share

    @book_value_per_share.setter
    def book_value_per_share(self, book_value_per_share):
        self._book_value_per_share = book_value_per_share

    def debug_info(self):
        info = self._stock
        info += " : revenue =>"
        info += str(self._revenue_in_millions)
        info += "\n net_income => "
        info += str(self._net_income_in_millions)
        info += "\n book_value => "
        info += str(self.book_value_per_share)
        return info

