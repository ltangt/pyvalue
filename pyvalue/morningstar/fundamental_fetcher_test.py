from pyvalue.morningstar import db
from pyvalue.morningstar import fundamental_fetcher
from pyvalue.morningstar import financial

fetcher = fundamental_fetcher.FundamentalFetcher()
share = financial.Financial('EQIX')
assert fetcher.fetch(share)

print share.debug_info()

# db = db.DB()
# db.connect()
# db.update(financial)
# db.close()

