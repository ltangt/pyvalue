import unittest
import morningstar_db
import stock_intrinsic_value
import constants


class StockIntrinsicValueTest(unittest.TestCase):

    @staticmethod
    def test_debt_to_assert_scorer():
        db = morningstar_db.MorningStartDB()
        db.connect()
        apple = db.retrieve('AAPL')
        apple_iv = stock_intrinsic_value.StockIntrinsicValue.intrinsic_value(apple)
        print apple_iv
        db.close()


if __name__ == '__main__':
    unittest.main()