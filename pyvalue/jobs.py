# The collection of jobs defined in this project
# Author: Liang Tang
# License: BSD
from pyvalue import constants
from pyvalue.morningstar.fetcher import Fetcher as MorningstarFetcher
from pyvalue.morningstar.financial import Financial as MorningstarFinancial
from pyvalue.morningstar.db import Database as MorningstarDB
from pyvalue.yahoofinance.db import Database as YahooFinancialDB
from pyvalue.yahoofinance.financial import Financial as YahooFinanceFinancial
from pyvalue.yahoofinance.fetcher import Fetcher as YahooFinanceFetcher
from pyvalue.log_info import LogInfo


def update_morningstar_fundamental(stock, overwrite=True, use_cache=False):
    fin = MorningstarFinancial(stock)
    success = MorningstarFetcher.fetch_fundamental(fin, use_cache=use_cache)
    if (fin is None) or (not success):
        LogInfo.info("No result")
        return
    print fin.debug_info()
    db_conn = MorningstarDB()
    db_conn.connect()
    db_conn.update_fundamentals(fin, overwrite=overwrite)
    db_conn.close()


def update_morningstar_stock_historical(stock, start_date, end_date, overwrite=True, use_cache=False):
    fin = MorningstarFinancial(stock)
    success = MorningstarFetcher.fetch_stock_historical(fin, start_date, end_date, use_cache=use_cache)
    if (fin is None) or (not success):
        LogInfo.info("No result")
        return
    print fin.debug_info()
    db_conn = MorningstarDB()
    db_conn.connect()
    db_conn.update_historical_stock_price(fin, overwrite=overwrite)
    db_conn.update_historical_dividend_date(fin, overwrite=overwrite)
    db_conn.close()


def update_sp500_morningstars_fundamental(columns=None, overwrite=True, use_cache=False):
    db_conn = MorningstarDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_sp_500_companies():
        fin = MorningstarFinancial(stock)
        success = MorningstarFetcher.fetch_fundamental(fin, use_cache=use_cache)
        log_msg = ""
        if (fin is None) or (not success):
            log_msg += "no result for " + stock + ", "
        else:
            ret = db_conn.update_fundamentals(fin, columns=columns, overwrite=overwrite)
            if ret:
                log_msg += "updated " + stock + ", "
            else:
                log_msg += "no update for " + stock + ", "
        log_msg += "total "+str(num_stock_updated+1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_sp500_morningstars_stock_historical(start_date, end_date, overwrite=True, use_cache=False):
    db_conn = MorningstarDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_sp_500_universe():
        fin = MorningstarFinancial(stock)
        success = MorningstarFetcher.fetch_stock_historical(fin, start_date, end_date, use_cache=use_cache)
        log_msg = ""
        if (fin is None) or (not success):
            log_msg += "no result for " + stock + ", "
        else:
            ret = db_conn.update_historical_stock_price(fin, overwrite=overwrite)
            ret |= db_conn.update_historical_dividend_date(fin, overwrite=overwrite)
            if ret:
                log_msg += "updated " + stock + ", "
            else:
                log_msg += "no update for " + stock + ", "
        log_msg += "total "+str(num_stock_updated+1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_nasdaq_eft_morningstar_stock_historical(start_date, end_date, overwrite=True, use_cache=False):
    db_conn = MorningstarDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_nasaq_efts_symbols():
        fin = MorningstarFinancial(stock)
        success = MorningstarFetcher.fetch_stock_historical(fin, start_date, end_date, use_cache=use_cache)
        log_msg = ""
        if (fin is None) or (not success):
            log_msg += "no result for " + stock + ", "
        else:
            ret = db_conn.update_historical_stock_price(fin, overwrite=overwrite)
            ret |= db_conn.update_historical_dividend_date(fin, overwrite=overwrite)
            if ret:
                log_msg += "updated " + stock + ", "
            else:
                log_msg += "no update for " + stock + ", "
        log_msg += "total " + str(num_stock_updated + 1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_yahoofinance_stock_quote(stock):
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    fin = YahooFinanceFinancial(stock)
    success = fetcher.fetch_quote(fin)
    log_msg = ""
    if not success:
        log_msg += "no result for " + stock
    else:
        db_conn.update_quote(fin)
        log_msg += "updated " + stock;
    log_msg += " , " + str(num_stock_updated + 1) + " stocks processed."
    LogInfo.info(log_msg)
    num_stock_updated += 1
    db_conn.close()

def update_sp500_yahoofinance_stock_quote():
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_sp_500_universe():
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_quote(fin)
        log_msg = ""
        if not success:
            log_msg += "no result for " + stock
        else:
            db_conn.update_quote(fin)
            log_msg += "updated " + stock;
        log_msg += " , "+str(num_stock_updated+1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_nasdaq_etf_yahoofinance_stock_quote():
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_nasaq_efts_symbols():
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_quote(fin)
        log_msg = ""
        if not success:
            log_msg += "no result for " + stock
        else:
            db_conn.update_quote(fin)
            log_msg += "updated " + stock;
        log_msg += " , "+str(num_stock_updated+1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_yahoofinance_stock_historical(stock, start_date, end_date):
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    fin = YahooFinanceFinancial(stock)
    success = fetcher.fetch_historical(fin, start_date, end_date)
    log_msg = ""
    if not success:
        log_msg += "no result for " + stock
    else:
        db_conn.update_historical(fin)
        log_msg += "updated " + stock
    log_msg += " , 1 stock processed."
    LogInfo.info(log_msg)
    db_conn.close()


def update_sp500_yahoofinance_stock_historical(start_date, end_date):
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_sp_500_universe():
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_historical(fin, start_date, end_date)
        log_msg = ""
        if not success:
            log_msg += "no result for " + stock
        else:
            db_conn.update_historical(fin)
            log_msg += "updated " + stock
        log_msg += " , "+str(num_stock_updated+1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()


def update_nasdaq_eft_yahoofinance_stock_historical(start_date, end_date):
    fetcher = YahooFinanceFetcher()
    db_conn = YahooFinancialDB()
    db_conn.connect()
    num_stock_updated = 0
    for stock in constants.get_nasaq_efts_symbols():
        fin = YahooFinanceFinancial(stock)
        success = fetcher.fetch_historical(fin, start_date, end_date)
        log_msg = ""
        if not success:
            log_msg += "no result for " + stock
        else:
            db_conn.update_historical(fin)
            log_msg += "updated " + stock
        log_msg += " , " + str(num_stock_updated + 1) + " stocks processed."
        LogInfo.info(log_msg)
        num_stock_updated += 1
    db_conn.close()
