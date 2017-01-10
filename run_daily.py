import sys
import os
import datetime

print "The daily job started at "+str(datetime.datetime.now())
print "Current directory is "+os.getcwd()
sys.path.append(os.getcwd())

import pyvalue.jobs as jobs
jobs.update_sp500_yahoofinance_stock_quote()
print "The daily job finished at "+str(datetime.datetime.now())