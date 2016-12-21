# Morningstar database interface
# Author: Liang Tang
# License: BSD
import pymysql
import datetime


class YahooFinanceDB:
    DB_ACCOUNT_FILE = "mysql_account.txt"
    DB_NAME = "investment"
    DB_TABLE = "yahoo_finance"
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
        cur = self._conn.cursor()
        cur.execute("SELECT STOCK, DATETIME FROM " + self.DB_TABLE
                    + " WHERE STOCK = '%s' AND VERSION = '%s'" % (stock, version))
        result = cur.fetchall()
        existing_dates = []
        for row in result:
            date = row[1].strftime('%Y-%m-%d %H:%M:%S')
            existing_dates.append(date)
        cur.close()
        existing_dates = set(existing_dates)
        # Insert to update the financial values in the database
        cur = self._conn.cursor()
        sql_insert = "INSERT INTO " + self.DB_TABLE + \
                     "  (STOCK, DATETIME, VERSION, " \
                     "  PRICE, DAYS_HIGH, DAYS_LOW, PRICE_CHANGE, " \
                     "  VOLUME, MARKET_CAP_IN_MILLIONS, BOOK_VALUE," \
                     "  EBITDA_IN_MILLIONS, DIVIDEND_SHARE, DIVIDEND_YIELD, EARNING_SHARE, " \
                     "  PRICE_BOOK, PRICE_SALES) " \
                     "VALUES('%s','%s','%s'," \
                     "  %s, " \
                     "  %s,%s,%s,%s," \
                     "  %s,%s,%s,%s," \
                     "  %s,%s,%s,%s )"
        sql_update = "UPDATE " + self.DB_TABLE + \
                     "SET PRICE = %s," \
                     "  DAYS_HIGH = %s, " \
                     "  DAYS_LOW = %s, " \
                     "  PRICE_CHANGE = %s, " \
                     "  VOLUME = %s, " \
                     "  MARKET_CAP_IN_MILLIONS = %s, " \
                     "  BOOK_VALUE = %s, " \
                     "  EBITDA_IN_MILLIONS = %s, " \
                     "  DIVIDEND_SHARE = %s, " \
                     "  DIVIDEND_YIELD = %s, " \
                     "  EARNING_SHARE = %s, " \
                     "  PRICE_BOOK = %s, " \
                     "  PRICE_SALES = %s, " \
                     "WHERE STOCK = '%s' AND DATE = '%s' " \
                     " AND VERSION = '%s'"
        cur_datetime = financial.datetime.strftime('%Y-%m-%d %H:%M:%S')
        value_tuple = (financial.price,
                       financial.days_high,
                       financial.days_low,
                       financial.price_change,
                       financial.volume,
                       financial.market_cap_in_millions,
                       financial.book_value,
                       financial.ebitda_in_millions,
                       financial.dividend_share,
                       financial.dividend_yield,
                       financial.earning_share,
                       financial.price_book,
                       financial.price_sales,
                       )
        value_tuple = YahooFinanceDB._process_tuple_value(value_tuple)
        if cur_datetime in existing_dates:
            value_tuple = value_tuple + (stock, cur_datetime, version)
            cur.execute(sql_update % value_tuple)
        else:
            value_tuple = (stock, cur_datetime, version) + value_tuple
            cur.execute(sql_insert % value_tuple)
        cur.close()
        self._conn.commit()

    @staticmethod
    def _process_tuple_value(value_tuple):
        new_list = []
        for val in value_tuple:
            if val is None:
                new_list.append("NULL")
            else:
                new_list.append("'"+str(val)+"'")
        return tuple(new_list)
