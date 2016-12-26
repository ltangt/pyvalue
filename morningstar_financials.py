# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD


class MorningStarFinancial(object):
    _stock = ""
    _revenue_mil = {}  # the key is the date and the value is the revenue in millions
    _revenue_currency = None  # the currency of the revenue, e.g., USD
    _net_income_mil = {}  # the key is the date and the value is the net income in millions
    _net_income_currency = None  # the currency of the net income, e.g., USD
    _book_value_per_share = {}  # the key is the date and the value is the book value per share
    _book_value_currency = None  # the currency of the book value, e.g., USD
    _share_mil = {}  # the total number of shares
    _operating_income_mil = {}  # the operating income in usd millions
    _operating_income_currency = None  # the currency of the operating income, e.g., USD
    _gross_margin = {}  # the gross margin, the difference between revenue and cost of goods sold divided by revenue
    _dividends = {}  # the dividend in usd per share
    _dividend_currency = None  # the currency of the dividend, e.g., USD
    _debt_to_equity = {}  # the debt/equity
    _current_ratio = {}  # the current ratio

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
    def revenue_currency(self):
        return self._revenue_currency

    @revenue_currency.setter
    def revenue_currency(self, value):
        self._revenue_currency = value

    @property
    def net_income_mil(self):
        return self._net_income_mil

    @net_income_mil.setter
    def net_income_mil(self, net_income):
        self._net_income_mil = net_income

    @property
    def net_income_currency(self):
        return self._net_income_currency

    @net_income_currency.setter
    def net_income_currency(self, value):
        self._net_income_currency = value

    @property
    def book_value_per_share(self):
        return self._book_value_per_share

    @book_value_per_share.setter
    def book_value_per_share(self, book_value_per_share):
        self._book_value_per_share = book_value_per_share

    @property
    def book_value_currency(self):
        return self._book_value_currency

    @book_value_currency.setter
    def book_value_currency(self, value):
        self._book_value_currency = value

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
    def operating_income_currency(self):
        return self._operating_income_currency

    @operating_income_currency.setter
    def operating_income_currency(self, value):
        self._operating_income_currency = value

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

    @property
    def dividend_currency(self):
        return self._dividend_currency

    @dividend_currency.setter
    def dividend_currency(self, value):
        self._dividend_currency = value

    @property
    def debt_to_equity(self):
        return self._debt_to_equity

    @debt_to_equity.setter
    def debt_to_equity(self, debt_to_equity):
        self._debt_to_equity = debt_to_equity

    @property
    def current_ratio(self):
        return self._current_ratio

    @current_ratio.setter
    def current_ratio(self, current_ratio):
        self._current_ratio = current_ratio

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
        info += str(self.operating_income_mil)
        info += "\n gross_margin => "
        info += str(self.gross_margin)
        info += "\n dividends => "
        info += str(self.dividends)
        info += "\n debt_to_equity => "
        info += str(self.debt_to_equity)
        info += "\n current_ratio => "
        info += str(self.current_ratio)
        return info

