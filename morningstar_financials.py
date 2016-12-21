# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD


class MorningStarFinancial(object):
    _stock = ""
    _revenue_mil = {}  # the key is the date and the value is the revenue in millions
    _net_income_mil = {}  # the key is the date and the value is the net income in millions
    _book_value_per_share = {}  # the key is the date and the value is the book value per share
    _share_mil = {}  # the total number of shares

    def __init__(self, stock, revenue = {}):
        self._stock = stock
        self._revenue_mil = revenue
        return

    @property
    def stock(self):
        return self._stock

    @property
    def revenue_mil(self):
        return self._revenue_mil

    @revenue_mil.setter
    def revenue_mil(self, revenue):
        self._revenue_mil = revenue

    @property
    def net_income_mil(self):
        return self._net_income_mil

    @net_income_mil.setter
    def net_income_mil(self, net_income):
        self._net_income_mil = net_income

    @property
    def book_value_per_share(self):
        return self._book_value_per_share

    @book_value_per_share.setter
    def book_value_per_share(self, book_value_per_share):
        self._book_value_per_share = book_value_per_share

    def debug_info(self):
        info = self._stock
        info += " : revenue =>"
        info += str(self._revenue_mil)
        info += "\n net_income => "
        info += str(self._net_income_mil)
        info += "\n book_value => "
        info += str(self.book_value_per_share)
        return info

