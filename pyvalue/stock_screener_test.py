import unittest

from pyvalue import stock_criteria
from pyvalue import stock_scorer
from pyvalue.stock_screener import StockScreener


class StockQueryTest(unittest.TestCase):

    def test_sp500(self):
        screener = StockScreener()
        iv_criteria = stock_criteria.StockScoreCriteria(stock_scorer.IntrinsicValueToMarketPrice())
        screener.add_criteria(iv_criteria)
        selected_stocks = screener.query_sp500()
        print "The selected stocks are : " + str(selected_stocks)

if __name__ == '__main__':
    unittest.main()
