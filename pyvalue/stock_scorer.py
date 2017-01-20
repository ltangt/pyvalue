# Score a stock based on various features
# Author: Liang Tang
# License: BSD
import datetime
from abc import ABCMeta, abstractmethod

from pyvalue.morningstar import financial
from pyvalue.stock_intrinsic_value import StockIntrinsicValue


class StockScorer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def score(self, fin, log=None):
        """
        Compute the score for a stock
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :return: the score
        """
        raise NotImplementedError()


def get_last_year_date():
    now = datetime.datetime.now()
    this_year = now.year
    return datetime.datetime(this_year - 1, now.month, now.day,
                             now.hour, now.month, now.second)


def date_values_after(date_values, start_date):
    """

    :param date_values: the dictionary of the data values, where the key is the date and the value is the value
    :type date_values: dict
    :param start_date:  the starting time
    :type start_date: datetime.datetime
    :return: a sub dictionary where the dates are after the start date
    """
    date_pairs = dict([(date_str, financial.convert_date(date_str)) for date_str in date_values.keys()])
    after_date_values = {}
    for date_str in date_pairs:
        date = date_pairs[date_str]
        if date >= start_date:
            after_date_values[date_str] = date_values[date_str]
    return after_date_values


class DebtToAssertScorer(StockScorer):
    def __init__(self, threshold=0.5, start_datetime=None):
        """

        :param threshold:
        :type threshold: float
        :param start_datetime:
        :type start_datetime: datetime.datetime
        """
        self._threshold = threshold
        if start_datetime is None:
            # Use the last year
            self._start_datetime = get_last_year_date()
        else:
            self._start_datetime = start_datetime

    def score(self, fin, log=None):
        """
        Compute the score for a stock
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: the score
        """
        valid_entries = date_values_after(fin.debt_to_equity, self._start_datetime)
        avg_debt_to_equity = sum([valid_entries.get(date_str) for date_str in valid_entries]) / len(valid_entries)
        score = 1.0 if avg_debt_to_equity <= self._threshold else 0.0
        return score


class CurrentRatioScorer(StockScorer):
    def __init__(self, threshold=1.5, start_datetime=None):
        """

        :param threshold:
        :type threshold: float
        :param start_datetime:
        :type start_datetime: datetime.datetime
        """
        self._threshold = threshold
        if start_datetime is None:
            # Use the last year
            self._start_datetime = get_last_year_date()
        else:
            self._start_datetime = start_datetime

    def score(self, fin, log):
        """
        Compute the score for a stock
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: the score
        """
        valid_entries = date_values_after(fin.current_ratio, self._start_datetime)
        avg_ratio = sum([valid_entries.get(date_str) for date_str in valid_entries]) / len(valid_entries)
        score = 1.0 if avg_ratio >= self._threshold else 0.0
        return score


class IntrinsicValueToMarketPrice(StockScorer):
    def __init__(self):
        pass

    def score(self, fin, log=None):
        """
        Compute the score for a stock
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: the score
        """
        iv = StockIntrinsicValue.intrinsic_value(fin)
        latest_price = fin.get_latest_price()
        if iv is None or latest_price is None:
            return None
        else:
            score = (iv - latest_price)/latest_price
            if log is not None:
                log.put(IntrinsicValueToMarketPrice, "score", score)
            return score
