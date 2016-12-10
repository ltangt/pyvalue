import pymysql
import datetime
import morningstar_financials

class MorningStartDB:
    DB_ACCOUNT_FILE = "mysql_account.txt"
    _db_server = ""
    _db_port = 0
    _db_username = ""
    _db_password = ""
    _conn = None

    def __init__(self):
        tmp_file = open(self.DB_ACCOUNT_FILE, "r")
        line = tmp_file.readlines()[0]
        [self._db_server, self._db_port, self._db_username, self._db_password] = line.split(",")
        self._db_server = self._db_server.strip()
        self._db_port = int(self._db_port.strip())
        self._db_username = self._db_username.strip()
        self._db_password = self._db_password.strip()
        tmp_file.close()
        return

    def connect(self):
        if self._conn is not None:
            print "already connected"
            return
        self._conn = pymysql.connect(host=self._db_server,
                                     port=self._db_port,
                                     user=self._db_username,
                                     passwd=self._db_password,
                                     db='morningstar')

    def close(self):
        self._conn.close()

    def update(self, financials, version='1'):
        revenue_in_millions = financials.revenue_in_millions
        stock = financials.stock
        cur = self._conn.cursor()
        sql = "INSERT INTO revenue(STOCK, DATE, VERSION, REVENUE_IN_MILLION	) VALUES('%s','%s','%s','%s')"
        for date in revenue_in_millions:
            revenue = revenue_in_millions[date]
            cur.execute(sql % (stock, self._formate_date(date), version, revenue))
        cur.close()
        self._conn.commit()

    def _formate_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y-%m')
            return date_str + "-01"
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
