# Morningstar database interface
# Author: Liang Tang
# License: BSD
import pymysql
import datetime


class MorningStartDB:
    DB_ACCOUNT_FILE = "mysql_account.txt"
    DB_NAME = "investment"
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
                                     db=self.DB_NAME)

    def close(self):
        self._conn.close()

    def update(self, financial, version='1'):
        stock = financial.stock
        self._update_date_values(stock, financial.revenue_mil, version,
                                 'morningstar_annual_revenue', 'REVENUE_MIL')
        self._update_date_values(stock, financial.net_income_mil, version,
                                 'morningstar_annual_net_income', 'NET_INCOME_MIL')
        self._update_date_values(stock, financial.book_value_per_share, version,
                                 'morningstar_book_value_per_share', 'BOOK_VALUE_PER_SHARE')
        self._conn.commit()

    # Update the revenue, net_income and other financial values with dates in the database
    def _update_date_values(self, stock, date_values, version, table_name, column_name):
        # extract the existing records of the stock and version
        cur = self._conn.cursor()
        cur.execute("SELECT STOCK, DATE FROM "+table_name+" WHERE STOCK = '%s' AND VERSION = '%s'" % (stock, version))
        result = cur.fetchall()
        existing_dates = []
        for row in result:
            date = row[1]
            existing_dates.append(date)
        cur.close()
        existing_dates = set(existing_dates)
        # Insert to update the financial values in the database
        cur = self._conn.cursor()
        sql_insert = "INSERT INTO " + table_name + "(STOCK, DATE, VERSION, " + column_name + \
                     ") VALUES('%s','%s','%s','%s')"
        sql_update = "UPDATE " + table_name + " SET "+column_name+" = '%s' WHERE STOCK = '%s' AND DATE = '%s' " \
                     " AND VERSION = '%s'"
        for date in date_values:
            value = date_values[date]
            if date in existing_dates:
                cur.execute(sql_update % (value, stock, date, version))
            else:
                cur.execute(sql_insert % (stock, date, version, value))
        cur.close()
