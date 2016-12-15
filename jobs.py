# The collection of jobs defined in this project
# Author: Liang Tang
# License: BSD

import morningstar_fetcher
import morningstar_db
import constants
import sys


def update_stock_morningstar(stock):
    fetcher = morningstar_fetcher.MorningStarFetcher()
    financial = fetcher.fetch(stock)
    print financial.debug_info()
    if financial is None:
        print "No result"
        return
    print financial.debug_info()
    db = morningstar_db.MorningStartDB()
    db.connect()
    db.update(financial)
    db.close()


def update_sp500_morningstars():
    fetcher = morningstar_fetcher.MorningStarFetcher()
    db = morningstar_db.MorningStartDB()
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


