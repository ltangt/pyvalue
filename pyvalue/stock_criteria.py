# Stock criteria
# Author: Liang Tang
# License: BSD
from abc import ABCMeta, abstractmethod


class StockCriteria:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def meet(self, fin, log=None):
        """
        Whether meet the stock criteria or not
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: whether the criteria is meet or not
        """
        raise NotImplementedError()


class StockScoreCriteria(StockCriteria):
    def __init__(self, scorer, threshold=0):
        """

        :param scorer: the scorer used by this filter
        :type scorer: pyvalue.stock_scorer.StockScorer
        :param threshold: the threshold for the scorer
        :type threshold: float
        """
        self._scorer = scorer
        self._threshold = threshold

    def meet(self, fin, log=None):
        return self._scorer.score(fin, log) >= self._threshold

