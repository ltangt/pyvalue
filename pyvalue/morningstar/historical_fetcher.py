# Morningstar stock price fetcher
# Author: Liang Tang
# License: BSD
import json
import os
import urllib2
import datetime

from pyvalue.morningstar import fetcher_exception
from pyvalue.morningstar import financial
from pyvalue.log_info import LogInfo


class HistoricalFetcher:
    PRICE_DATA_LIST = "PriceDataList"
    VOLUME_LIST = "VolumeList"
    DATA_POINTS = "Datapoints"
    DATE_INDEXS = "DateIndexs"
    DIVIDEND_DATA = "DividendData"
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
                if use_cache and HistoricalFetcher._has_cache(filename):
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
                success = HistoricalFetcher._parse_json(json_text, fin)
                if success:
                    return True
            except Exception as err:
                LogInfo.info(stock + " : " + err.message + " in the "+str((try_idx+1))+" time for "+stock)
                if try_idx == num_retries - 1:
                    LogInfo.error('Failed to retrieve information for '+stock)
                    return False

    @staticmethod
    def _has_cache(filename):
        if not os.path.isfile(filename):
            return False
        tmp_file = open(filename, "r")
        content = tmp_file.read()
        tmp_file.close()
        return len(content) > 0

    @staticmethod
    def _parse_json(json_text, fin):
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

        # Parse the PriceDataList
        if not HistoricalFetcher._parse_price_data(json_obj, fin):
            return False
        # Parse the DividendData
        if not HistoricalFetcher._parse_dividend_data(json_obj, fin):
            return False

        return True

    @staticmethod
    def _parse_price_data(json_obj, fin):
        """
        Extract the Price data from the parsed JSON object into the financial object
        :param json_obj: the parsed json object
        :type json_obj: dict
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :return: whether success or not
        """
        stock = fin.stock
        if HistoricalFetcher.PRICE_DATA_LIST not in json_obj:
            raise fetcher_exception.FetcherException(HistoricalFetcher.PRICE_DATA_LIST
                                                     + " is not in the json response for " + stock)
        if HistoricalFetcher.VOLUME_LIST not in json_obj:
            raise fetcher_exception.FetcherException(HistoricalFetcher.VOLUME_LIST
                                                     + " is not in the json response for " + stock)
        price_data_list = json_obj[HistoricalFetcher.PRICE_DATA_LIST]
        if len(price_data_list) == 0:
            raise fetcher_exception.FetcherException(HistoricalFetcher.PRICE_DATA_LIST + " is empty for " + stock)
        price_data = price_data_list[0]
        if HistoricalFetcher.DATA_POINTS not in price_data:
            raise fetcher_exception.FetcherException(HistoricalFetcher.DATA_POINTS + " is not in the "
                                                     + HistoricalFetcher.PRICE_DATA_LIST + " for " + stock)
        price_data_points = price_data[HistoricalFetcher.DATA_POINTS]
        if HistoricalFetcher.DATE_INDEXS not in price_data:
            raise fetcher_exception.FetcherException(HistoricalFetcher.DATE_INDEXS + " is not in the "
                                                     + HistoricalFetcher.PRICE_DATA_LIST + "for " + stock)
        date_indexes = price_data[HistoricalFetcher.DATE_INDEXS]
        num_points = len(price_data_points)

        volume_data_list = json_obj[HistoricalFetcher.VOLUME_LIST]
        if HistoricalFetcher.DATA_POINTS not in volume_data_list:
            raise fetcher_exception.FetcherException(HistoricalFetcher.DATA_POINTS + " is not in the "
                                                    + HistoricalFetcher.VOLUME_LIST + " for " + stock)
        volume_data_points = volume_data_list[HistoricalFetcher.DATA_POINTS]
        assert num_points == len(date_indexes)
        assert num_points == len(volume_data_points)
        close_prices = {}
        highest_prices = {}
        lowest_prices = {}
        open_prices = {}
        volumes = {}
        for idx in range(num_points):
            date_index = date_indexes[idx]
            date_str = HistoricalFetcher._convert_to_date(date_index)
            price_point = price_data_points[idx]
            assert len(price_point) == 4
            [close_price, highest_price, lowest_price, open_price] = price_point
            close_prices[date_str] = close_price
            highest_prices[date_str] = highest_price
            lowest_prices[date_str] = lowest_price
            open_prices[date_str] = open_price
            volumes[date_str] = float(volume_data_points[idx]) * 1000 * 1000
        fin.stock_daily_close_price = close_prices
        fin.stock_daily_highest_price = highest_prices
        fin.stock_daily_lowest_price = lowest_prices
        fin.stock_daily_open_price = open_prices
        fin.stock_daily_price_currency = 'USD'
        fin.stock_daily_volume = volumes
        return True

    @staticmethod
    def _parse_dividend_data(json_obj, fin):
        """
        Extract the Dividend data from the parsed JSON object into the financial object
        :param json_obj: the parsed json object
        :type json_obj: dict
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :return: whether success or not
        """
        stock = fin.stock
        if HistoricalFetcher.DIVIDEND_DATA not in json_obj:
            raise fetcher_exception.FetcherException(HistoricalFetcher.DIVIDEND_DATA
                                                     + " is not in the json response for " + stock)
        dividend_data = json_obj[HistoricalFetcher.DIVIDEND_DATA]
        dividends = {}
        num_points = len(dividend_data)
        for idx in range(num_points):
            record = dividend_data[idx]
            dividend_date = record["Date"]
            dividend_type = record["Type"]
            if dividend_type == "Dividend":
                desc = record["Desc"]  # e.g., "Dividends:0.5200"
                tokens = desc.split(":")
                div_str = tokens[1].strip().replace("<br>", "")
                dividends[dividend_date] = float(div_str)  # e.g., 0.5200
        fin.stock_dividend_date = dividends
        return True

    @staticmethod
    def _convert_to_date(date_index):
        """
        Conver the date index to a date string in the format of "YYYY-MM-dd"
        :param date_index: the date index
        :type date_index: int
        :return: the date string in the format of "YYYY-MM-dd"
        """
        date_time = HistoricalFetcher.START_DATE + datetime.timedelta(days=date_index)
        return date_time.strftime("%Y-%m-%d")
