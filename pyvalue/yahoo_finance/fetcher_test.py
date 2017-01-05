from pyvalue.yahoo_finance import fetcher
from pyvalue.yahoo_finance import db

fetcher = fetcher.Fetcher()
fin = fetcher.fetch('EQIX')
print fin.debug_info()

db_conn = db.Database()
db_conn.connect()
db_conn.update(fin)
db_conn.close()
