import unittest
from pyvalue.morningstar import db
from pyvalue.morningstar import financial
from pyvalue.morningstar.fetcher import Fetcher


class DatabaseTest(unittest.TestCase):

    # def test_retrieve_fundamentals(self):
    #     db_conn = db.Database()
    #     db_conn.connect()
    #     apple = financial.Financial('AAPL')
    #     self.assertTrue(db_conn.retrieve_fundamentals(apple))
    #     print apple.debug_info()
    #     self.assertTrue(len(apple.revenue_mil) > 0)
    #     db_conn.close()
    #
    # def test_retrieve_historical_prices(self):
    #     db_conn = db.Database()
    #     db_conn.connect()
    #     apple = financial.Financial('AAPL')
    #     self.assertTrue(db_conn.retrieve_historical_prices(apple))
    #     print apple.debug_info()
    #     self.assertTrue(len(apple.stock_daily_close_price) > 0)
    #     db_conn.close()

    def test_update_historical_prices(self):
        fetcher = Fetcher()
        aapl = financial.Financial('AAPL')
        fetcher.fetch_stock_historical(aapl, '2016-01-01', '2017-02-01')
        db_conn = db.Database()
        db_conn.connect()
        db_conn.update_historical_stock_price(aapl)
        db_conn.update_historical_dividend_date(aapl)
        db_conn.close()

if __name__ == '__main__':
    unittest.main()
