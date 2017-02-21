import unittest

from pyvalue.morningstar import financial
from pyvalue.morningstar import historical_fetcher


class StockPriceFetcherTest(unittest.TestCase):

    @staticmethod
    def test_fetcher():
        apple = financial.Financial('AAPL')
        fetcher = historical_fetcher.HistoricalFetcher()
        fetcher.fetch(apple, '2017-1-3', '2017-1-3')
        print apple.debug_info()

if __name__ == '__main__':
    unittest.main()
