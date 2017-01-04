import yahoo_finance_fetcher as fetcher
import yahoo_finance_db as db

fetcher = fetcher.YahooFinanceFetcher()
financial = fetcher.fetch('EQIX')
print financial.debug_info()

db = db.YahooFinanceDB()
db.connect()
db.update(financial)
db.close()
