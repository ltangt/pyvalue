import unittest

import financial
import stock_price_fetcher


class StockPriceFetcherTest(unittest.TestCase):

    @staticmethod
    def test_fetcher():
        apple = financial.Financial('AAPL')
        fetcher = stock_price_fetcher.StockPriceFetcher()
        fetcher.fetch(apple, '2017-1-3', '2017-1-3')
        print apple.debug_info()

if __name__ == '__main__':
    unittest.main()
