from pyvalue.yahoofinance import fetcher
from pyvalue.yahoofinance import db
from pyvalue.yahoofinance import financial

fetcher = fetcher.Fetcher()
fin = financial.Financial('AAPL')
# fetcher.fetch_historical(fin, '2016-12-01', '2017-01-05')
fetcher.fetch_quote(fin)
print fin.debug_info()

db_conn = db.Database()
db_conn.connect()
db_conn.update_quote(fin)
db_conn.close()


#db_conn = db.Database()
#db_conn.connect()
#db_conn.update_historical(fin)
#db_conn.close()
