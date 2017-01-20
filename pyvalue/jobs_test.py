from pyvalue import jobs

# jobs.update_morningstar_fundamental('AAPL')
# jobs.update_morningstar_stock_historical('AAPL', '2016-07-01', '2017-01-03')
# jobs.update_sp500_morningstars_stock_price()
# jobs.update_morningstar_fundamental('ACE')
# jobs.update_sp500_morningstars_fundamental()
# jobs.update_sp500_morningstars_fundamental(overwrite=False, use_cache=True)
# jobs.update_sp500_yahoofinance_stock_quote()
# jobs.update_sp500_yahoofinance_stock_historical('2016-01-01', '2017-01-04')
jobs.update_morningstar_stock_historical('SPY', '2014-07-01', '2017-01-18')
jobs.update_yahoofinance_stock_historical('SPY', '2014-07-01', '2017-01-18')
