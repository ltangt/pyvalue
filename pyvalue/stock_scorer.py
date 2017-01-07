# Score a stock based on various features
# Author: Liang Tang
# License: BSD
import datetime
from abc import ABCMeta, abstractmethod

from pyvalue.morningstar import financial


class StockScorer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def score(self, f):
        """
        Compute the score for a stock
        :param f: the morningstar financial object of the stock
        :type f: financial.Financial
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

    def score(self, f):
        """
        Compute the score for a stock
        :param f: the morningstar financial object of the stock
        :type f: financial.Financial
        :return: the score
        """
        valid_entries = date_values_after(f.debt_to_equity, self._start_datetime)
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

    def score(self, f):
        """
        Compute the score for a stock
        :param f: the morningstar financial object of the stock
        :type f: financial.Financial
        :return: the score
        """
        valid_entries = date_values_after(f.current_ratio, self._start_datetime)
        avg_ratio = sum([valid_entries.get(date_str) for date_str in valid_entries]) / len(valid_entries)
        score = 1.0 if avg_ratio >= self._threshold else 0.0
        return score
