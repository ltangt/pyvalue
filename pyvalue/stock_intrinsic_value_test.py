import unittest
import sys
from pyvalue.stock_intrinsic_value import StockIntrinsicValue
from pyvalue.morningstar import db
from pyvalue.morningstar import financial
from pyvalue import constants


class StockIntrinsicValueTest(unittest.TestCase):

    def test_single_stock(self):
        db_conn = db.Database()
        db_conn.connect()
        apple = financial.Financial('AAPL')
        db_conn.retrieve_fundamentals(apple)
        apple_iv = StockIntrinsicValue.intrinsic_value(apple, debug=True)
        self.assertTrue(apple_iv is not None)
        print apple_iv
        db_conn.close()

    def test_sp500_stocks(self):
        db_conn = db.Database()
        db_conn.connect()
        for stock in constants.SP500_2015_10:
            fin = financial.Financial(stock)
            self.assertTrue(db_conn.retrieve_fundamentals(fin))
            self.assertTrue(db_conn.retrieve_historical_prices(fin))
            iv = StockIntrinsicValue.intrinsic_value(fin)
            latest_price = fin.get_latest_price()
            if len(fin.stock_daily_close_price) == 0:
                print stock + " : no latest price "
            elif iv is None:
                print stock+" : latest price : " + str(latest_price) + ", intrinsic value : None"
            else:
                print stock+" : latest price : " + str(latest_price) + ", intrinsic value : "+str(iv) \
                      + " diff: "+str(iv-latest_price)
        db_conn.close()


if __name__ == '__main__':
    unittest.main()
