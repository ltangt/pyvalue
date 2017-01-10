# Query stock based on strategies
# Author: Liang Tang
# License: BSD
import constants
from pyvalue.morningstar.db import Database as MorningStarDB
from pyvalue.morningstar.financial import Financial as MorningStarFinancial
from pyvalue.stock_query_filter import StockQueryFilter
from pyvalue.log_info import LogInfo
from pyvalue.stock_scorer import IntrinsicValueToMarketPrice


class StockQuery:
    def __init__(self):
        self._filters = []

    def add_filter(self, f):
        """

        :param filter
        :type filter: pyvalue.stock_query_filter.StockQueryFilter
        :return:
        """
        if not isinstance(f, StockQueryFilter):
            raise ValueError("the filter must be an instance of "+StockQueryFilter.__name__)
        self._filters.append(f)

    def query_sp500(self, debug=False):
        """
        query over the SP 500 stocks
        :param debug: whether use the debug mode or not
        :return:
        """
        results = []
        db = MorningStarDB()
        db.connect()
        log_info = LogInfo()
        num_stock_scanned = 0
        for stock in constants.SP500_2015_10:
            fin = MorningStarFinancial(stock)
            num_stock_scanned += 1
            if db.retrieve_fundamentals(fin) and db.retrieve_historical_prices(fin):
                should_keep = True
                for tmp_filter in self._filters:
                    if not tmp_filter.filter(fin, log_info):
                        should_keep = False
                        break
                if should_keep:
                    results.append(stock)
                    print "selected "+stock + ", score = "+str(log_info.get(IntrinsicValueToMarketPrice, "score"))
            if num_stock_scanned%10 == 0:
                print str(num_stock_scanned) + " stocks were scanned."
        db.close()
        return results

