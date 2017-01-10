import unittest

from pyvalue.stock_query_filter import StockQueryFilter
from pyvalue import stock_query_filter
from pyvalue import stock_scorer
from pyvalue.stock_query import StockQuery
from pyvalue.morningstar import financial
from pyvalue.morningstar import db


class StockQueryTest(unittest.TestCase):

    def test_sp500(self):
        query_portal = StockQuery()
        iv_filter = stock_query_filter.StockScoreFilter(stock_scorer.IntrinsicValueToMarketPrice())
        query_portal.add_filter(iv_filter)
        selected_stocks = query_portal.query_sp500()
        print "The selected stocks are : " + str(selected_stocks)

if __name__ == '__main__':
    unittest.main()
