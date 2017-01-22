# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD
import datetime


class Financial(object):
    def __init__(self, stock):
        self._stock = stock
        # All the properties (except for the currency) are the dictionary data structure,
        # where the key is the date in form of "YYYY-mm-dd" and the value is actual value.
        self._revenue_mil = {}  # the key is the date and the value is the revenue in millions
        self._revenue_currency = None  # the currency of the revenue, e.g., USD
        self._net_income_mil = {}  # the key is the date and the value is the net income in millions
        self._net_income_currency = None  # the currency of the net income, e.g., USD
        self._free_cash_flow_mil = {}  # the key is the date and the value is the free cash flow in millions
        self._free_cash_flow_currency = None  # the currency of the free cash flow, e.g., USD
        self._book_value_per_share = {}  # the key is the date and the value is the book value per share
        self._book_value_currency = None  # the currency of the book value, e.g., USD
        self._share_mil = {}  # the total number of shares
        self._operating_income_mil = {}  # the operating income in usd millions
        self._operating_income_currency = None  # the currency of the operating income, e.g., USD
        self._gross_margin = {}  # the gross margin, the difference between revenue and cost of goods sold divided
        # by revenue
        self._dividends = {}  # the dividend in usd per share
        self._dividend_currency = None  # the currency of the dividend, e.g., USD
        self._debt_to_equity = {}  # the debt/equity
        self._current_ratio = {}  # the current ratio
        self._stock_daily_close_price = {}  # the historical close price for each day
        self._stock_daily_open_price = {}  # the historical open price for each day
        self._stock_daily_highest_price = {}  # the historical highest price for each day
        self._stock_daily_lowest_price = {}  # the historical lowest price for each day
        self._stock_daily_price_currency = None  # the currency of the stock price for each day
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
    def free_cash_flow_mil(self):
        return self._free_cash_flow_mil

    @free_cash_flow_mil.setter
    def free_cash_flow_mil(self, free_cash_flow):
        self._free_cash_flow_mil = free_cash_flow

    @property
    def free_cash_flow_currency(self):
        return self._free_cash_flow_currency

    @free_cash_flow_currency.setter
    def free_cash_flow_currency(self, value):
        self._free_cash_flow_currency = value

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

    @property
    def stock_daily_open_price(self):
        return self._stock_daily_open_price

    @stock_daily_open_price.setter
    def stock_daily_open_price(self, value):
        self._stock_daily_open_price = value

    @property
    def stock_daily_close_price(self):
        return self._stock_daily_close_price

    @stock_daily_close_price.setter
    def stock_daily_close_price(self, value):
        self._stock_daily_close_price = value

    @property
    def stock_daily_highest_price(self):
        return self._stock_daily_highest_price

    @stock_daily_highest_price.setter
    def stock_daily_highest_price(self, value):
        self._stock_daily_highest_price = value

    @property
    def stock_daily_lowest_price(self):
        return self._stock_daily_lowest_price

    @stock_daily_lowest_price.setter
    def stock_daily_lowest_price(self, value):
        self._stock_daily_lowest_price = value

    @property
    def stock_daily_price_currency(self):
        return self._stock_daily_price_currency

    @stock_daily_price_currency.setter
    def stock_daily_price_currency(self, value):
        self._stock_daily_price_currency = value

    def get_latest_price(self):
        if len(self.stock_daily_close_price) == 0:
            return None
        sorted_dates = sorted(self.stock_daily_close_price.keys(), cmp=cmp_date)
        return self.stock_daily_close_price[sorted_dates[-1]]

    def debug_info(self):
        info = self._stock
        info += " : revenue =>"
        info += str(self._revenue_mil)
        info += "\n net_income => "
        info += str(self._net_income_mil)
        info += "\n free_cash_flow => "
        info += str(self._free_cash_flow_mil)
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
        info += "\n stock_daily_price_currency => "
        info += str(self.stock_daily_price_currency)
        info += "\n stock_daily_close_price =>"
        info += str(self.stock_daily_close_price)
        info += "\n stock_daily_open_price =>"
        info += str(self.stock_daily_open_price)
        info += "\n stock_daily_highest_price =>"
        info += str(self.stock_daily_highest_price)
        info += "\n stock_daily_lowest_price =>"
        info += str(self.stock_daily_lowest_price)
        return info


def convert_date(date_text):
    """
    Convert the date text into the python datetime object
    :param date_text: the date text read from morningstar
    :type date_text: str
    :return: the converted datatime
    """
    if date_text == "TTM":
        return datetime.datetime.now()
    elif date_text == "Latest Qtr":
        now = datetime.datetime.now();
        last_qrt = now - datetime.timedelta(days=120)
        return last_qrt
    else:
        try:
            return datetime.datetime.strptime(date_text, "%Y-%m")
        except:
            return datetime.datetime.strptime(date_text, "%Y-%m-%d")

def cmp_date(date_text1, date_text2):
    """
    Compare two date strings, which are the keys of the financial date values
    :param date_text1:
    :type date1: str
    :param date_text2:
    :type date_text2: str
    :return:
    """
    date1 = convert_date(date_text1)
    date2 = convert_date(date_text2)
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1
