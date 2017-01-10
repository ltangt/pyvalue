import unittest
from pyvalue.morningstar import db
from pyvalue.morningstar import financial


class DatabaseTest(unittest.TestCase):

    def test_retrieve_fundamentals(self):
        db_conn = db.Database()
        db_conn.connect()
        apple = financial.Financial('AAPL')
        self.assertTrue(db_conn.retrieve_fundamentals(apple))
        print apple.debug_info()
        self.assertTrue(len(apple.revenue_mil) > 0)
        db_conn.close()

    def test_retrieve_historical_prices(self):
        db_conn = db.Database()
        db_conn.connect()
        apple = financial.Financial('AAPL')
        self.assertTrue(db_conn.retrieve_historical_prices(apple))
        print apple.debug_info()
        self.assertTrue(len(apple.stock_daily_close_price) > 0)
        db_conn.close()

if __name__ == '__main__':
    unittest.main()
