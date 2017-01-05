from pyvalue import yahoo_finance_fetcher as fetcher
from pyvalue import yahoo_finance_db as db

fetcher = fetcher.YahooFinanceFetcher()
financial = fetcher.fetch('EQIX')
print financial.debug_info()

db_conn = db.YahooFinanceDB()
db_conn.connect()
db_conn.update(financial)
db_conn.close()
