# Morningstar stock price fetcher
# Author: Liang Tang
# License: BSD
import json
import os
import sys
import urllib2
import datetime

from pyvalue.morningstar import fetcher_exception
from pyvalue.morningstar import financial


class StockPriceFetcher:
    PRICE_DATA_LIST = "PriceDataList"
    DATA_POINTS = "Datapoints"
    DATE_INDEXS = "DateIndexs"
    START_DATE = datetime.datetime.strptime("1900-01-01", "%Y-%m-%d")

    def __init__(self):
        return

    def fetch(self, fin, start_date, end_date, num_retries=3, use_cache=False):
        """
        Fetch the fundamental data of a security
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param start_date: the start date
        :type start_date: str
        :param end_date: the end date
        :type end_date: str
        :param num_retries: the number of retries
        :type num_retries: int
        :param use_cache: whether to use cache if cache exists
        :type use_cache: bool
        :return: whether success or not
        """
        stock = fin.stock
        url = (r'http://globalquote.morningstar.com/globalcomponent/RealtimeHistoricalStockData.ashx?'
               r'ticker={0}&showVol=true&dtype=his&f=d&curry=USD'
               r'&range={1}|{2}&isD=true&isS=true&hasF=true&ProdCode=DIRECT'.format(
                   stock, start_date, end_date))
        for try_idx in range(num_retries):
            try:
                filename = "/tmp/" + stock + "_prices.json"
                if use_cache and StockPriceFetcher.__has_cache(filename):
                    tmp_file = open(filename, "r")
                    json_text = tmp_file.read()
                    tmp_file.close()
                else:
                    response = urllib2.urlopen(url)
                    json_text = response.read()
                    if len(json_text.strip()) == 0 or json_text.strip() == 'null':
                        raise fetcher_exception.FetcherException("Empty response of the http request for "+stock)
                    tmp_file = open(filename, "w")
                    tmp_file.write(json_text)
                    tmp_file.close()
                success = StockPriceFetcher.__parse_json(json_text, fin)
                if success:
                    return True
            except (fetcher_exception.FetcherException, urllib2.HTTPError) as err:
                print stock + " : " + err.message + " in the "+str((try_idx+1))+" time for "+stock
                if try_idx == num_retries - 1:
                    sys.stderr.write('Failed to retrieve information for '+stock+'\n')
                    return False

    @staticmethod
    def __has_cache(filename):
        if not os.path.isfile(filename):
            return False
        tmp_file = open(filename, "r")
        content = tmp_file.read()
        tmp_file.close()
        return len(content) > 0

    @staticmethod
    def __parse_json(json_text, fin):
        """
        Parse the json response from the morningstar
        :param json_text: the json response
        :type json_text: str
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :return: whether success or not
        """
        stock = fin.stock
        try:
            json_obj = json.loads(json_text)
        except ValueError:
            raise fetcher_exception.FetcherException("Decoding JSON has failed for "+stock)

        if json_obj is None:
            raise fetcher_exception.FetcherException("Decoding JSON has failed for "+stock)

        if StockPriceFetcher.PRICE_DATA_LIST not in json_obj:
            raise fetcher_exception.FetcherException(StockPriceFetcher.PRICE_DATA_LIST
                                                     + " is not in the json response for "+stock)
        price_data_list = json_obj[StockPriceFetcher.PRICE_DATA_LIST]
        if len(price_data_list) == 0:
            raise fetcher_exception.FetcherException(StockPriceFetcher.PRICE_DATA_LIST + " is empty for "+stock)
        price_data = price_data_list[0]
        if StockPriceFetcher.DATA_POINTS not in price_data:
            raise fetcher_exception.FetcherException(StockPriceFetcher.DATA_POINTS+" is not in the "
                                                     + StockPriceFetcher.PRICE_DATA_LIST + "for "+stock)
        data_points = price_data[StockPriceFetcher.DATA_POINTS]
        if StockPriceFetcher.DATE_INDEXS not in price_data:
            raise fetcher_exception.FetcherException(StockPriceFetcher.DATE_INDEXS + " is not in the "
                                                     + StockPriceFetcher.PRICE_DATA_LIST + "for "+stock)
        date_indexes = price_data[StockPriceFetcher.DATE_INDEXS]
        num_points = len(data_points)
        assert num_points == len(date_indexes)
        close_prices = {}
        higest_prices = {}
        lowest_prices = {}
        open_prices = {}
        for idx in range(num_points):
            date_index = date_indexes[idx]
            date_str = StockPriceFetcher.__convert_to_date(date_index)
            date_point = data_points[idx]
            assert len(date_point) == 4
            [close_price, higest_price, lowest_price, open_price] = date_point
            close_prices[date_str] = close_price
            higest_prices[date_str] = higest_price
            lowest_prices[date_str] = lowest_price
            open_prices[date_str] = open_price
        fin.stock_daily_close_price = close_prices
        fin.stock_daily_highest_price = higest_prices
        fin.stock_daily_lowest_price = lowest_prices
        fin.stock_daily_open_price = open_prices
        fin.stock_daily_price_currency = 'USD'
        return True

    @staticmethod
    def __convert_to_date(date_index):
        """
        Conver the date index to a date string in the format of "YYYY-MM-dd"
        :param date_index: the date index
        :type date_index: int
        :return: the date string in the format of "YYYY-MM-dd"
        """
        date_time = StockPriceFetcher.START_DATE + datetime.timedelta(days=date_index)
        return date_time.strftime("%Y-%m-%d")







