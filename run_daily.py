import sys
import os
import datetime

print "====================="
print str(datetime.datetime.now())+": the daily job has started"
print "Current directory is "+os.getcwd()
sys.path.append(os.getcwd())

import pyvalue.jobs as jobs
#jobs.update_sp500_yahoofinance_stock_quote()
jobs.update_nasdaq_etf_yahoofinance_stock_quote()
print "====================="
print str(datetime.datetime.now())+": the daily job has finished"
