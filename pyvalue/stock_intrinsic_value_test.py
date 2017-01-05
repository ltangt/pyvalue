import unittest
from pyvalue import stock_intrinsic_value
from pyvalue.morningstar import db


class StockIntrinsicValueTest(unittest.TestCase):

    @staticmethod
    def test_debt_to_assert_scorer():
        db_conn = db.DB()
        db_conn.connect()
        apple = db_conn.retrieve('AAPL')
        apple_iv = stock_intrinsic_value.StockIntrinsicValue.intrinsic_value(apple)
        print apple_iv
        db_conn.close()


if __name__ == '__main__':
    unittest.main()
