import sys
import os

print "Current directory is "+os.getcwd()
sys.path.append(os.getcwd())

import pyvalue.jobs as jobs
jobs.update_sp500_morningstars_stock_price('2016-01-01', '2017-01-03')
