import jobs

#jobs.update_stock_morningstar('AAPL')
#jobs.update_sp500_morningstars()
jobs.update_sp500_morningstars(["OPERATING_INCOME_MIL", "GROSS_MARGIN", "DIVIDENDS"])
#jobs.update_sp500_yahoofinance()