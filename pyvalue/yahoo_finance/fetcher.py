# Yahoo finance api data fetcher
# Author: Liang Tang
# License: BSD
import datetime
from yahoo_finance import Share
from pyvalue.yahoo_finance.financials import Financial
from dateutil.parser import parse


class YahooFinanceFetcherException(Exception):
    pass


class Fetcher:
    def __init__(self):
        self._num_retries = 3
        return

    def fetch(self, stock, num_retries=3):
        self._num_retries = num_retries
        share = Share(stock)
        return self._fetch(stock, share)

    def _fetch(self, stock, share):
        f = Financial(stock)
        f.trade_datetime = parse(share.get_trade_datetime())
        f.price = self._float_val(share, "get_price")
        f.days_high = self._float_val(share, "get_days_high")
        f.days_low = self._float_val(share, "get_days_low")
        f.change = self._float_val(share, "get_change")
        f.volume = self._float_val(share, "get_volume")
        f.market_cap_in_millions = self._parse_number_in_millions(share, "get_market_cap")
        f.book_value = self._float_val(share, "get_book_value")
        f.ebitda_in_millions = self._parse_number_in_millions(share, "get_ebitda")
        f.dividend_share = self._float_val(share, "get_dividend_share")
        f.dividend_yield = self._float_val(share, "get_dividend_yield")
        f.earning_share = self._float_val(share, "get_earnings_share")
        f.price_book = self._float_val(share, "get_price_book")
        f.price_sales = self._float_val(share, "get_price_sales")
        return f

    def _parse_number_in_millions(self, share, attr_name):
        val = self._text_val(share, attr_name)
        if val is None:
            return None
        val = val.strip()
        if val.endswith("B"):
            return float(val[:-1])*1000
        elif val.endswith("M"):
            return float(val[:-1])
        elif val.endswith("K"):
            return float(val[:-1])/1000.0
        else:
            return float(val[:-1])/(1000.0*1000.0)

    def _text_val(self, share, attr_name):
        method = getattr(share, attr_name)
        val = None
        for try_idx in range(self._num_retries):
            try:
                val = method()
                if val is not None:
                    break
            except YahooFinanceFetcherException:
                pass
        return val

    def _float_val(self, share, attr_name):
        val = self._text_val(share, attr_name)
        if val is None:
            return None
        else:
            return float(val)

