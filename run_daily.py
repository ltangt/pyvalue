import sys
import os

print "Current directory is "+os.getcwd()
sys.path.append(os.getcwd())

import pyvalue.jobs as jobs
jobs.update_sp500_yahoofinance_stock_quote()