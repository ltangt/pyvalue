import morningstar_fetcher as fetcher
import morningstar_db as db


fetcher = fetcher.MorningStarFetcher()
financial = fetcher.fetch('EQIX')

print financial.debug_info()

db = db.MorningStartDB()
db.connect()
db.update(financial)
db.close()

