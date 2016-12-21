# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD


class MorningStarFinancial(object):
    _stock = ""
    _revenue_mil = {}  # the key is the date and the value is the revenue in millions
    _net_income_mil = {}  # the key is the date and the value is the net income in millions
    _book_value_per_share = {}  # the key is the date and the value is the book value per share
    _share_mil = {}  # the total number of shares
    _operating_income_mil = {}  # the operating income in usd millions
    _gross_margin = {}  # the gross margin, the difference between revenue and cost of goods sold divided by revenue
    _dividends = {}  # the diviend in usd per share

    def __init__(self, stock, revenue={}):
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

    @property
    def share_mil(self):
        return self._share_mil

    @share_mil.setter
    def share_mil(self, share_mil):
        self._share_mil = share_mil

    @property
    def operating_income_mil(self):
        return self._operating_income_mil

    @operating_income_mil.setter
    def operating_income_mil(self, operating_income):
        self._operating_income_mil = operating_income

    @property
    def gross_margin(self):
        return self._gross_margin

    @gross_margin.setter
    def gross_margin(self, gross_margin):
        self._gross_margin = gross_margin

    @property
    def dividends(self):
        return self._dividends

    @dividends.setter
    def dividends(self, dividends):
        self._dividends = dividends

    def debug_info(self):
        info = self._stock
        info += " : revenue =>"
        info += str(self._revenue_mil)
        info += "\n net_income => "
        info += str(self._net_income_mil)
        info += "\n book_value => "
        info += str(self.book_value_per_share)
        info += "\n share_mil => "
        info += str(self.share_mil)
        info += "\n operating_income => "
        info += str(self.operating_income)
        info += "\n gross_margin => "
        info += str(self.gross_margin)
        info += "\n dividends => "
        info += str(self.dividends)
        return info

