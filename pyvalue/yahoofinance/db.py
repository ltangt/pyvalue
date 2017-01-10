# Morningstar database interface
# Author: Liang Tang
# License: BSD
import pymysql
from pyvalue import config
from pyvalue.log_info import LogInfo


class Database:
    DB_NAME = "investment"
    STOCK_QUOTE_TABLE = "yahoo_finance_stock_quote"
    STOCK_HISTORICAL_TABLE = "yahoo_finance_stock_historical"

    def __init__(self):
        config.init()
        self._db_server = config.config.get("mysql", "server").strip()
        self._db_port = int(config.config.get("mysql", "port").strip())
        self._db_username = config.config.get("mysql", "username").strip()
        self._db_password = config.config.get("mysql", "password").strip()
        self._conn = None

    def connect(self):
        if self._conn is not None:
            LogInfo.info("already connected")
            return
        self._conn = pymysql.connect(host=self._db_server,
                                     port=self._db_port,
                                     user=self._db_username,
                                     passwd=self._db_password,
                                     db=self.DB_NAME)

    def close(self):
        self._conn.close()

    def update_quote(self, fin, version='1'):
        stock = fin.stock
        if stock is None:
            LogInfo.error("the stock is None")
            return False
        if fin.trade_datetime is None:
            LogInfo.error(stock+" : the trade datetime is None")
            return False
        cur = self._conn.cursor()
        cur.execute("SELECT STOCK, TRADE_DATETIME_UTC FROM " + self.STOCK_QUOTE_TABLE
                    + " WHERE STOCK = '%s' AND VERSION = '%s'" % (stock, version))
        result = cur.fetchall()
        existing_datetimes = []
        for row in result:
            date = row[1].strftime('%Y-%m-%d %H:%M:%S')
            existing_datetimes.append(date)
        cur.close()
        existing_datetimes = set(existing_datetimes)
        # Insert to update the financial values in the database
        cur = self._conn.cursor()
        sql_insert = "INSERT INTO " + Database.STOCK_QUOTE_TABLE + \
                     "  (STOCK, TRADE_DATETIME_UTC, VERSION, " \
                     "  PRICE, DAYS_HIGH, DAYS_LOW, PRICE_CHANGE, " \
                     "  VOLUME, MARKET_CAP_IN_MILLIONS, BOOK_VALUE," \
                     "  EBITDA_IN_MILLIONS, DIVIDEND_SHARE, DIVIDEND_YIELD, EARNING_SHARE, " \
                     "  PRICE_BOOK, PRICE_SALES) " \
                     "VALUES('%s','%s','%s'," \
                     "  %s, " \
                     "  %s,%s,%s,%s," \
                     "  %s,%s,%s,%s," \
                     "  %s,%s,%s,%s )"
        sql_update = "UPDATE " + Database.STOCK_QUOTE_TABLE + " " + \
                     "SET TS=CURRENT_TIMESTAMP(), " \
                     "  PRICE = %s," \
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
                     "  PRICE_SALES = %s " \
                     "WHERE STOCK = '%s' AND TRADE_DATETIME_UTC = '%s' " \
                     " AND VERSION = '%s'"
        cur_datetime = fin.trade_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Only works for UTC timezone
        value_tuple = (fin.price,
                       fin.days_high,
                       fin.days_low,
                       fin.price_change,
                       fin.volume,
                       fin.market_cap_in_millions,
                       fin.book_value,
                       fin.ebitda_in_millions,
                       fin.dividend_share,
                       fin.dividend_yield,
                       fin.earning_share,
                       fin.price_book,
                       fin.price_sales,
                       )
        value_tuple = Database._process_tuple_value(value_tuple)
        if cur_datetime in existing_datetimes:
            value_tuple += (stock, cur_datetime, version)
            cur.execute(sql_update % value_tuple)
        else:
            value_tuple = (stock, cur_datetime, version) + value_tuple
            cur.execute(sql_insert % value_tuple)
        cur.close()
        self._conn.commit()

    def update_historical(self, fin, version='1'):
        """
        Insert and update the historical daily price
        :param fin: the financial object
        :type fin: pyvalue.yahoofinance.financial.Financial
        :param version:
        :return:
        """
        stock = fin.stock
        # Check whether the historical daily record is empty or not
        daily_records = fin.stock_historical
        if daily_records is None or len(daily_records) == 0:
            return 0
        # Select the existing records
        cur = self._conn.cursor()
        cur.execute("SELECT STOCK, DATE FROM " + self.STOCK_HISTORICAL_TABLE
                    + " WHERE STOCK = '%s' AND VERSION = '%s'" % (stock, version))
        result = cur.fetchall()
        existing_dates = []
        for row in result:
            normalized_date_text = row[1].strftime("%Y-%m-%d")
            existing_dates.append(normalized_date_text)
        cur.close()
        existing_dates = set(existing_dates)
        # Insert to update the financial values in the database
        cur = self._conn.cursor()
        sql_insert = "INSERT INTO " + Database.STOCK_HISTORICAL_TABLE + \
                     "  (STOCK, DATE, VERSION, " \
                     "  CLOSE, OPEN, LOW, HIGH, ADJ_CLOSE, VOLUME) " \
                     "VALUES('%s','%s','%s'," \
                     "  %s,%s,%s,%s,%s,%s)"
        sql_update = "UPDATE " + Database.STOCK_HISTORICAL_TABLE + " " + \
                     "SET TS=CURRENT_TIMESTAMP(), " \
                     "  CLOSE = %s," \
                     "  OPEN = %s, " \
                     "  LOW = %s, " \
                     "  HIGH = %s, " \
                     "  ADJ_CLOSE = %s, " \
                     "  VOLUME = %s " \
                     "WHERE STOCK = '%s' AND DATE = '%s' " \
                     " AND VERSION = '%s'"
        for record in daily_records:
            value_tuple = (record.close, record.open, record.low, record.high, record.adj_close, record.volume)
            value_tuple = Database._process_tuple_value(value_tuple)
            normalized_date_text = record.date.strftime("%Y-%m-%d")
            if normalized_date_text in existing_dates:
                value_tuple += (stock, record.date, version)
                cur.execute(sql_update % value_tuple)
            else:
                value_tuple = (stock, record.date, version) + value_tuple
                cur.execute(sql_insert % value_tuple)
        cur.close()
        self._conn.commit()
        return len(daily_records)

    @staticmethod
    def _process_tuple_value(value_tuple):
        new_list = []
        for val in value_tuple:
            if val is None:
                new_list.append("NULL")
            else:
                new_list.append("'"+str(val)+"'")
        return tuple(new_list)
