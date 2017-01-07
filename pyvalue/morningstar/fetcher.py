# Morningstar data fetcher
# Author: Liang Tang
# License: BSD
from pyvalue.morningstar import fundamental_fetcher
from pyvalue.morningstar import stock_price_fetcher


class Fetcher:
    def __init__(self):
        return

    @staticmethod
    def fetch_fundamental(fin, num_retries=3, use_cache=False):
        internal_fetcher = fundamental_fetcher.FundamentalFetcher()
        return internal_fetcher.fetch(fin, num_retries=num_retries, use_cache=use_cache)

    @staticmethod
    def fetch_stock_historical_price(fin, start_date, end_date, num_retries=3, use_cache=False):
        internal_fetcher = stock_price_fetcher.StockPriceFetcher()
        return internal_fetcher.fetch(fin, start_date, end_date, num_retries=num_retries, use_cache=use_cache)


