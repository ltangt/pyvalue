# The data structure of the monrningstar financial objects
# Author: Liang Tang
# License: BSD
import datetime


class MorningStarFinancial(object):
    __stock = ""
    __revenue_mil = {}  # the key is the date and the value is the revenue in millions
    __revenue_currency = None  # the currency of the revenue, e.g., USD
    __net_income_mil = {}  # the key is the date and the value is the net income in millions
    __net_income_currency = None  # the currency of the net income, e.g., USD
    __book_value_per_share = {}  # the key is the date and the value is the book value per share
    __book_value_currency = None  # the currency of the book value, e.g., USD
    __share_mil = {}  # the total number of shares
    __operating_income_mil = {}  # the operating income in usd millions
    __operating_income_currency = None  # the currency of the operating income, e.g., USD
    __gross_margin = {}  # the gross margin, the difference between revenue and cost of goods sold divided by revenue
    __dividends = {}  # the dividend in usd per share
    __dividend_currency = None  # the currency of the dividend, e.g., USD
    __debt_to_equity = {}  # the debt/equity
    __current_ratio = {}  # the current ratio

    def __init__(self, stock, revenue={}):
        self.__stock = stock
        self.__revenue_mil = revenue
        return

    @property
    def stock(self):
        return self.__stock

    @property
    def revenue_mil(self):
        return self.__revenue_mil

    @revenue_mil.setter
    def revenue_mil(self, revenue):
        self.__revenue_mil = revenue

    @property
    def revenue_currency(self):
        return self.__revenue_currency

    @revenue_currency.setter
    def revenue_currency(self, value):
        self.__revenue_currency = value

    @property
    def net_income_mil(self):
        return self.__net_income_mil

    @net_income_mil.setter
    def net_income_mil(self, net_income):
        self.__net_income_mil = net_income

    @property
    def net_income_currency(self):
        return self.__net_income_currency

    @net_income_currency.setter
    def net_income_currency(self, value):
        self.__net_income_currency = value

    @property
    def book_value_per_share(self):
        return self.__book_value_per_share

    @book_value_per_share.setter
    def book_value_per_share(self, book_value_per_share):
        self.__book_value_per_share = book_value_per_share

    @property
    def book_value_currency(self):
        return self.__book_value_currency

    @book_value_currency.setter
    def book_value_currency(self, value):
        self.__book_value_currency = value

    @property
    def share_mil(self):
        return self.__share_mil

    @share_mil.setter
    def share_mil(self, share_mil):
        self.__share_mil = share_mil

    @property
    def operating_income_mil(self):
        return self.__operating_income_mil

    @operating_income_mil.setter
    def operating_income_mil(self, operating_income):
        self.__operating_income_mil = operating_income

    @property
    def operating_income_currency(self):
        return self.__operating_income_currency

    @operating_income_currency.setter
    def operating_income_currency(self, value):
        self.__operating_income_currency = value

    @property
    def gross_margin(self):
        return self.__gross_margin

    @gross_margin.setter
    def gross_margin(self, gross_margin):
        self.__gross_margin = gross_margin

    @property
    def dividends(self):
        return self.__dividends

    @dividends.setter
    def dividends(self, dividends):
        self.__dividends = dividends

    @property
    def dividend_currency(self):
        return self.__dividend_currency

    @dividend_currency.setter
    def dividend_currency(self, value):
        self.__dividend_currency = value

    @property
    def debt_to_equity(self):
        return self.__debt_to_equity

    @debt_to_equity.setter
    def debt_to_equity(self, debt_to_equity):
        self.__debt_to_equity = debt_to_equity

    @property
    def current_ratio(self):
        return self.__current_ratio

    @current_ratio.setter
    def current_ratio(self, current_ratio):
        self.__current_ratio = current_ratio

    def debug_info(self):
        info = self.__stock
        info += " : revenue =>"
        info += str(self.__revenue_mil)
        info += "\n net_income => "
        info += str(self.__net_income_mil)
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
        return datetime.datetime.strptime(date_text, "%Y-%m")


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
