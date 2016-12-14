# Morningstar database interface
# Author: Liang Tang
# License: BSD
import pymysql
import datetime


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

    def update(self, financial, version='1'):
        revenue_in_millions = financial.revenue_in_millions
        stock = financial.stock
        # extract the existing records of the stock and version
        cur = self._conn.cursor()
        cur.execute("SELECT STOCK, DATE FROM revenue WHERE STOCK = '%s' AND VERSION = '%s'" % (stock, version))
        result = cur.fetchall()
        existing_dates = []
        for row in result:
            date = row[1].strftime('%Y-%m-%d')
            existing_dates.append(date)
        cur.close()
        existing_dates = set(existing_dates)

        cur = self._conn.cursor()
        sql_insert = "INSERT INTO revenue(STOCK, DATE, VERSION, REVENUE_IN_MILLION	) VALUES('%s','%s','%s','%s')"
        sql_update = "UPDATE revenue SET REVENUE_IN_MILLION = '%s' WHERE STOCK = '%s' AND DATE = '%s' " \
                     " AND VERSION = '%s'"

        for date in revenue_in_millions:
            revenue = revenue_in_millions[date]
            date_format = self._formate_date(date)
            if date_format in existing_dates:
                cur.execute(sql_update % (revenue, stock, date_format, version))
            else:
                cur.execute(sql_insert % (stock, date_format, version, revenue))
        cur.close()
        self._conn.commit()

    def _formate_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y-%m')
            return date_str + "-01"
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
