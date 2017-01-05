# The collection of jobs defined in this project
# Author: Liang Tang
# License: BSD

import sys
import datetime
from pyvalue import constants
from pyvalue import yahoo_finance_db
from pyvalue import yahoo_finance_fetcher
from pyvalue.morningstar import fundamental_fetcher, stock_price_fetcher, financial, db


def daily_job():
    update_sp500_morningstars_fundamental()


def update_stock_morningstar_fundamental(stock, overwrite=True, use_cache=False):
    fetcher = fundamental_fetcher.FundamentalFetcher()
    fin = financial.Financial(stock)
    success = fetcher.fetch(fin, use_cache=False)
    if (fin is None) or (not success):
        print "No result"
        return
    print fin.debug_info()
    db_conn = db.DB()
    db_conn.connect()
    db_conn.update_fundamentals(fin, overwrite=overwrite)
    db_conn.close()


def update_stock_morningstar_stock_price(stock, start_date, end_date, overwrite=True, use_cache=False):
    fetcher = stock_price_fetcher.StockPriceFetcher()
    fin = financial.Financial(stock)
    success = fetcher.fetch(fin, start_date, end_date, use_cache=False)
    if (fin is None) or (not success):
        print "No result"
        return
    print fin.debug_info()
    db_conn = db.DB()
    db_conn.connect()
    db_conn.update_stock_prices(fin, overwrite=overwrite)
    db_conn.close()


def update_sp500_morningstars_fundamental(columns=None, overwrite=True, use_cache=False):
    fetcher = fundamental_fetcher.FundamentalFetcher()
    db_conn = db.DB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.sp500_2015_10:
        fin = financial.Financial(stock)
        success = fetcher.fetch(fin, use_cache=use_cache)
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
    fetcher = stock_price_fetcher.StockPriceFetcher()
    db_conn = db.DB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.sp500_2015_10:
        fin = financial.Financial(stock)
        success = fetcher.fetch(fin, start_date, end_date, use_cache=use_cache)
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

