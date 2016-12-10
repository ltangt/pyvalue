import morningstar_fetcher as fetcher
import morningstar_db as db

fetcher = fetcher.MorningStarFetcher()
financials = fetcher.fetch('AAPL')

print financials.debug_info()

db = db.MorningStartDB()
db.connect()
db.update(financials)
db.close()

