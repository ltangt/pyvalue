# The collection of jobs defined in this project
# Author: Liang Tang
# License: BSD

import sys

from pyvalue import constants
from pyvalue.morningstar.fetcher import Fetcher as MorningstarFetcher
from pyvalue.morningstar.financial import Financial as MorningstarFinancial
from pyvalue.morningstar.db import Database as MorningstarDB
from pyvalue.yahoofinance.db import Database as YahooFinancialDB
from pyvalue.yahoofinance.financial import Financial as YahooFinanceFinancial
from pyvalue.yahoofinance.fetcher import Fetcher as YahooFinanceFetcher


def daily_job():
    update_sp500_morningstars_fundamental()


def update_stock_morningstar_fundamental(stock, overwrite=True, use_cache=False):
    fin = MorningstarFinancial(stock)
    success = MorningstarFetcher.fetch_fundamental(fin, use_cache=False)
    if (fin is None) or (not success):
        print "No result"
        return
    print fin.debug_info()
    db_conn = MorningstarDB()
    db_conn.connect()
    db_conn.update_fundamentals(fin, overwrite=overwrite)
    db_conn.close()


def update_stock_morningstar_stock_price(stock, start_date, end_date, overwrite=True, use_cache=False):
    fin = MorningstarFinancial(stock)
    success = MorningstarFetcher.fetch_stock_historical_price(fin, start_date, end_date, use_cache=False)
    if (fin is None) or (not success):
        print "No result"
        return
    print fin.debug_info()
    db_conn = MorningstarDB()
    db_conn.connect()
    db_conn.update_stock_prices(fin, overwrite=overwrite)
    db_conn.close()


def update_sp500_morningstars_fundamental(columns=None, overwrite=True, use_cache=False):
    db_conn = MorningstarDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.SP500_2015_10:
        fin = MorningstarFinancial(stock)
        success = MorningstarFetcher.fetch_fundamental(fin, use_cache=use_cache)
        if (fin is None) or (not success):
            sys.stdout.write("no result for " + stock + ", ")
        else:
            ret = db_conn.update_fundamentals(fin, columns=columns, overwrite=overwrite)
            if ret:
                sys.stdout.write("updated " + stock + ", ")
            else:
                sys.stdout.write("no update for " + stock + ", ")
        sys.stdout.write("total "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db_conn.close()


def update_sp500_morningstars_stock_price(start_date, end_date, overwrite=True, use_cache=False):
    db_conn = MorningstarDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.SP500_2015_10:
        fin = MorningstarFinancial(stock)
        success = MorningstarFetcher.fetch_stock_historical_price(fin, start_date, end_date, use_cache=use_cache)
        if (fin is None) or (not success):
            sys.stdout.write("no result for " + stock + ", ")
        else:
            ret = db_conn.update_stock_prices(fin, overwrite=overwrite)
            if ret:
                sys.stdout.write("updated " + stock + ", ")
            else:
                sys.stdout.write("no update for " + stock + ", ")
        sys.stdout.write("total "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db_conn.close()


def update_sp500_yahoofinance_stock_quote():
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.SP500_2015_10:
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_quote(fin)
        if not success:
            sys.stdout.write("no result for " + stock)
        else:
            db_conn.update_quote(fin)
            sys.stdout.write("updated " + stock)
        sys.stdout.write(" , "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db_conn.close()


def update_sp500_yahoofinance_stock_historical(start_date, end_date):
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.SP500_2015_10:
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_historical(fin, start_date, end_date)
        if not success:
            sys.stdout.write("no result for " + stock)
        else:
            db_conn.update_historical(fin)
            sys.stdout.write("updated " + stock)
        sys.stdout.write(" , "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db_conn.close()

