# The collection of jobs defined in this project
# Author: Liang Tang
# License: BSD

import morningstar_fetcher
import morningstar_db
import yahoo_finance_fetcher
import yahoo_finance_db
import constants
import sys


def daily_job():
    update_sp500_morningstars()


def update_stock_morningstar(stock, overwrite=True, use_cache=False):
    fetcher = morningstar_fetcher.MorningStarFetcher()
    financial = fetcher.fetch(stock, use_cache=False)
    print financial.debug_info()
    if financial is None:
        print "No result"
        return
    print financial.debug_info()
    db = morningstar_db.MorningStartDB()
    db.connect()
    db.update(financial, overwrite=overwrite)
    db.close()


def update_sp500_morningstars(columns=None, overwrite=True, use_cache=False):
    fetcher = morningstar_fetcher.MorningStarFetcher()
    db = morningstar_db.MorningStartDB()
    db.connect()
    num_stock_updated = 0
    for stock in constants.sp500_2015_10:
        financial = fetcher.fetch(stock, use_cache=use_cache)
        if financial is None:
            sys.stdout.write("no result for " + stock + ", ")
        else:
            ret = db.update(financial, columns=columns, overwrite=overwrite)
            if ret:
                sys.stdout.write("updated " + stock + ", ")
            else:
                sys.stdout.write("no update for " + stock + ", ")
        sys.stdout.write("total "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db.close()


def update_sp500_yahoofinance():
    fetcher = yahoo_finance_fetcher.YahooFinanceFetcher()
    db = yahoo_finance_db.YahooFinanceDB()
    db.connect()
    num_stock_updated = 0
    for stock in constants.sp500_2015_10:
        financial = fetcher.fetch(stock)
        if financial is None:
            sys.stdout.write("no result for " + stock)
        else:
            db.update(financial)
            sys.stdout.write("updated " + stock)
        sys.stdout.write(" , "+str(num_stock_updated+1) + " stocks processed. \n")
        num_stock_updated += 1
    db.close()
