# Yahoo finance api data fetcher
# Author: Liang Tang
# License: BSD
import sys

import datetime
from yahoo_finance import Share
from dateutil.parser import parse
from pyvalue.yahoofinance.financial import DailyRecord
from pyvalue.log_info import LogInfo


class YahooFinanceFetcherException(Exception):
    pass


class Fetcher:
    def __init__(self):
        self._num_retries = 3
        return

    def fetch_quote(self, fin, num_retries=3):
        stock = fin.stock
        self._num_retries = num_retries
        for try_idx in range(num_retries):
            try:
                share = Share(stock)
                self._fetch_quote(fin, share)
                return True
            except YahooFinanceFetcherException as err:
                LogInfo.info(stock + " : " + err.message + " in the " + str((try_idx + 1)) + " time")
                if try_idx == num_retries - 1:
                    LogInfo.error('Failed to retrieve information for ' + stock )
                    return False

    def _fetch_quote(self, f, share):
        stock = f.stock
        trade_datetime_text = self._text_val(share, "get_trade_datetime")
        if trade_datetime_text is None:
            raise YahooFinanceFetcherException(stock + " does not has trading time.")
        f.trade_datetime = parse(trade_datetime_text)
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

    def fetch_historical(self, fin, start_date, end_date, num_retries=3):
        stock = fin.stock
        self._num_retries = num_retries
        for try_idx in range(num_retries):
            try:
                share = Share(stock)
                ret = Fetcher._fetch_historical(fin, share, start_date, end_date)
                if ret == 0:
                    raise YahooFinanceFetcherException("historical result is empty")
                return True
            except YahooFinanceFetcherException as err:
                LogInfo.info(stock + " : " + err.message + " in the " + str((try_idx + 1)) + " time")
                if try_idx == num_retries - 1:
                    sys.stderr.write('Failed to retrieve information for ' + stock + '\n')
                    return False

    @staticmethod
    def _fetch_historical(fin, share, start_date, end_date):
        """
        fetch the Yahoo Finance historical api data
        :param fin: the financial object
        :type fin: pyvalue.yahoofinance.financial.Financial
        :param share: the share object from yahoo finance python library
        :type share: Share
        :param start_date: the start date
        :type start_date: str
        :param end_date: the end date
        :type end_date: str
        :return: the number of daily records fetched
        """

        hist = Fetcher._get_historical(share, start_date, end_date)
        if hist is None or len(hist) == 0:
            raise YahooFinanceFetcherException("no result")
        daily_records = []
        for elem in hist:
            record = DailyRecord()
            date_text = elem['Date']
            record.date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
            record.open = elem['Open']
            record.close = elem['Close']
            record.adj_close = elem['Adj_Close']
            record.high = elem['High']
            record.low = elem['Low']
            record.volume = elem['Volume']
            daily_records.append(record)
        fin.stock_historical = daily_records
        return len(fin.stock_historical)

    @staticmethod
    def _parse_number_in_millions(share, attr_name):
        val = Fetcher._text_val(share, attr_name)
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

    @staticmethod
    def _text_val(share, attr_name):
        method = getattr(share, attr_name)
        try:
            return method()
        except:
            return None

    @staticmethod
    def _float_val(share, attr_name):
        val = Fetcher._text_val(share, attr_name)
        if val is None:
            return None
        else:
            return float(val)

    @staticmethod
    def _get_historical(share, start_date, end_date, step_days=356):
        """
        get the historical stock price from Yahoo Finance api
        :param share:
        :type share: yahoo_finance.Share
        :param start_date:
        :param end_date:
        :param step_days:
        :return:
        """
        mask = '%Y-%m-%d'
        start = datetime.datetime.strptime(start_date, mask)
        end = datetime.datetime.strptime(end_date, mask)
        result = []
        if start > end:
            raise ValueError('Start date "%s" is greater than "%s"' % (start_date, end_date))
        step = datetime.timedelta(days=step_days)
        while end - step > start:
            current = end - step
            try:
                hist = share.get_historical(current.strftime(mask), end.strftime(mask))
                result.extend(hist)
            except:
                pass
            end = current - datetime.timedelta(days=1)
        else:
            try:
                hist = share.get_historical(start.strftime(mask), end.strftime(mask))
                result.extend(hist)
            except:
                pass
        return result

