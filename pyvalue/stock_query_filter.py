# Stock query filter
# Author: Liang Tang
# License: BSD
from abc import ABCMeta, abstractmethod


class StockQueryFilter:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def filter(self, f, log=None):
        """
        Compute the score for a stock
        :param f: the morningstar financial object of the stock
        :type f: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: whether the condition is satisfied or not
        """
        raise NotImplementedError()


class StockScoreFilter(StockQueryFilter):
    def __init__(self, scorer, threshold=0):
        """

        :param scorer: the scorer used by this filter
        :type scorer: pyvalue.stock_scorer.StockScorer
        :param threshold: the threshold for the scorer
        :type threshold: float
        """
        self._scorer = scorer
        self._threshold = threshold

    def filter(self, f, log=None):
        return self._scorer.score(f, log) >= self._threshold

