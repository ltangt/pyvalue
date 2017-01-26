# Yahoo finance api data fetcher
# Author: Liang Tang
# License: BSD
import datetime
import urllib2
from dateutil.parser import parse

from pyvalue.yahoofinance.financial import DailyRecord
from pyvalue.log_info import LogInfo


class YahooFinanceFetcherException(Exception):
    pass


class Fetcher:
    def __init__(self):
        return

    def fetch_quote(self, f, num_retries=3):
        """
        Directly call Yahoo Finance website to get the stock quote.
        See Details: http://wern-ancheta.com/blog/2015/04/05/getting-started-with-the-yahoo-finance-api/
        :param f: the financial object
        :type f: pyvalue.yahoofinance.financial.Financial
        :param num_retries: the number of retries
        :type num_retries: int
        :return:
        """
        stock = f.stock
        url = (r'http://finance.yahoo.com/d/quotes.csv?s={0}&f=d1t1l1ghc1vj1b4j4dyep6p5'.format(stock))
        for try_idx in range(num_retries):
            try:
                response = urllib2.urlopen(url)
                csv = response.read()
                if len(csv.strip()) == 0:
                    raise YahooFinanceFetcherException("Empty response of the http request.")
                self._parse_quote_csv(csv, f)
                return True
            except Exception as err:
                LogInfo.info(stock + " : " + err.message + " in the " + str((try_idx + 1)) + " time")
                if try_idx == num_retries - 1:
                    LogInfo.error('Failed to retrieve information for ' + stock)
                    return False

    def _parse_quote_csv(self, csv, f):
        """
        :param csv: the return csv data from Yahoo finance
        :type csv: str
        :param f: the financial object
        :type f: pyvalue.yahoofinance.financial.Financial
        :return:
        """
        stock = f.stock
        data = csv.split(',')
        column_idx = 0
        trade_datetime_text = (data[column_idx] + " " + data[column_idx+1]).replace('"', '')
        if trade_datetime_text is None:
            raise YahooFinanceFetcherException(stock + " does not has trading time.")
        f.trade_datetime = parse(trade_datetime_text)
        column_idx += 2
        f.price = float(data[column_idx])
        column_idx += 1
        f.days_low = float(data[column_idx])
        column_idx += 1
        f.days_high = float(data[column_idx])
        column_idx += 1
        f.change = float(data[column_idx])
        column_idx += 1
        f.volume = float(data[column_idx])
        column_idx += 1
        f.market_cap_in_millions = self._parse_number_in_millions(data[column_idx])
        column_idx += 1
        f.book_value = float(data[column_idx])
        column_idx += 1
        f.ebitda_in_millions = self._parse_number_in_millions(data[column_idx])
        column_idx += 1
        f.dividend_share = float(data[column_idx])
        column_idx += 1
        f.dividend_yield = float(data[column_idx])
        column_idx += 1
        f.earning_share = float(data[column_idx])
        column_idx += 1
        f.price_book = float(data[column_idx])
        column_idx += 1
        f.price_sales = float(data[column_idx])
        return True

    def fetch_historical(self, f, start_date, end_date, num_retries=3):
        """

        :param f: the financial object
        :type f: pyvalue.yahoofinance.financial.Financial
        :param start_date: the start date
        :type start_date: str
        :param end_date: the end data
        :type end_date: str
        :param num_retries: the number of retries
        :type num_retries: int
        :return:
        """
        stock = f.stock
        start_year, start_month, start_day = Fetcher._parse_date_str(start_date)
        end_year, end_month, end_day = Fetcher._parse_date_str(end_date)
        url = (r'http://ichart.finance.yahoo.com/table.csv?s={0}'
               r'&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv'
               .format(stock, start_month-1, start_day, start_year, end_month-1, end_day, end_year))
        for try_idx in range(num_retries):
            try:
                response = urllib2.urlopen(url)
                csv = response.read()
                if len(csv.strip()) == 0:
                    raise YahooFinanceFetcherException("Empty response of the http request.")
                self._parse_historical_csv(csv, f)
                return True
            except Exception as err:
                LogInfo.info(stock + " : " + err.message + " in the " + str((try_idx + 1)) + " time")
                if try_idx == num_retries - 1:
                    LogInfo.error('Failed to retrieve information for ' + stock)
                    return False

    def _parse_historical_csv(self, csv, f):
        """
        :param csv: the return csv data from Yahoo finance
        :type csv: str
        :param f: the financial object
        :type f: pyvalue.yahoofinance.financial.Financial
        :return:
        """
        lines = csv.split('\n')[1:] # skip the first line (header)
        daily_records = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            elems = line.split(',')
            record = DailyRecord()
            column_idx = 0
            date_text = elems[column_idx]
            record.date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
            column_idx += 1
            record.open = elems[column_idx]
            column_idx += 1
            record.high = elems[column_idx]
            column_idx += 1
            record.low = elems[column_idx]
            column_idx += 1
            record.close = elems[column_idx]
            column_idx += 1
            record.volume = elems[column_idx]
            column_idx += 1
            record.adj_close = elems[column_idx]
            daily_records.append(record)
            f.stock_historical = daily_records
        return len(f.stock_historical)

    @staticmethod
    def _parse_number_in_millions(val):
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
    def _parse_date_str(date_str):
        tokens = date_str.split('-')
        year = int(tokens[0])
        month = int(tokens[1])
        day = int(tokens[2])
        return year, month, day

