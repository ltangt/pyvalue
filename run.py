import sys
import os

print "Current directory is "+os.getcwd()
sys.path.append(os.getcwd())

import pyvalue.jobs as jobs
#jobs.update_sp500_morningstars_stock_price('2016-01-01', '2017-01-03')
#jobs.update_sp500_yahoofinance_stock_historical('2014-01-01', '2014-12-31')
jobs.update_morningstar_stock_historical('VAR','2010-01-01', '2012-12-31')
#jobs.update_yahoofinance_stock_historical('VAR', '2010-01-01', '2012-12-31')
#jobs.update_sp500_yahoofinance_stock_quote()