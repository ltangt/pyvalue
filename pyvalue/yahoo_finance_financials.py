# Yahoo finance api data structure
# Author: Liang Tang
# License: BSD


class YahooFinanceFinancial(object):
    _stock = ""
    _trade_datetime = None
    _price = None
    _days_high = None
    _days_low = None
    _price_change = None
    _volume = None
    _market_cap_in_millions = None
    _book_value = None
    _ebitda_in_millions = None
    _dividend_share = None
    _dividend_yield = None
    _earning_share = None
    _price_book = None
    _price_sales = None

    def __init__(self, stock):
        self._stock = stock
        return

    @property
    def stock(self):
        return self._stock

    @property
    def trade_datetime(self):
        return self._trade_datetime

    @trade_datetime.setter
    def trade_datetime(self, datetime):
        self._trade_datetime = datetime

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def days_high(self):
        return self._days_high

    @days_high.setter
    def days_high(self, days_high):
        self._days_high = days_high

    @property
    def days_low(self):
        return self._days_low

    @days_low.setter
    def days_low(self, days_low):
        self._days_low = days_low

    @property
    def price_change(self):
        return self._price_change

    @price_change.setter
    def price_change(self, price_change):
        self._price_change = price_change

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

    @property
    def market_cap_in_millions(self):
        return self._market_cap_in_millions

    @market_cap_in_millions.setter
    def market_cap_in_millions(self, market_cap_in_millions):
        self._market_cap_in_millions = market_cap_in_millions

    @property
    def book_value(self):
        return self._book_value

    @book_value.setter
    def book_value(self, book_value):
        self._book_value = book_value

    @property
    def ebitda_in_millions(self):
        return self._ebitda_in_millions

    @ebitda_in_millions.setter
    def ebitda_in_millions(self, ebitda_in_millions):
        self._ebitda_in_millions = ebitda_in_millions

    @property
    def dividend_share(self):
        return self._dividend_share

    @dividend_share.setter
    def dividend_share(self, dividend_share):
        self._dividend_share = dividend_share

    @property
    def dividend_yield(self):
        return self._dividend_yield

    @dividend_yield.setter
    def dividend_yield(self, dividend_yield):
        self._dividend_yield = dividend_yield

    @property
    def earning_share(self):
        return self._earning_share

    @earning_share.setter
    def earning_share(self, earning_share):
        self._earning_share = earning_share

    @property
    def price_book(self):
        return self._price_book

    @price_book.setter
    def price_book(self, price_book):
        self._price_book = price_book

    @property
    def price_sales(self):
        return self._price_sales

    @price_sales.setter
    def price_sales(self, price_sales):
        self._price_sales = price_sales

    def debug_info(self):
        info = self._stock
        info += " : datetime =>"
        info += str(self.trade_datetime)
        info += "\n price => "
        info += str(self.price)
        info += "\n days_high => "
        info += str(self.days_high)
        info += "\n days_low => "
        info += str(self.days_low)
        info += "\n market_cap => "
        info += str(self.market_cap_in_millions)
        return info

