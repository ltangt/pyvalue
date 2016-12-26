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

    def update(self, financial, version='1', columns=None, overwrite=True):
        stock = financial.stock
        # The key is the column name, the value is a tuple of value attribute, currency attribute, and the table name
        table_columns = {
            'REVENUE_MIL': ('revenue_mil', 'revenue_currency', 'morningstar_annual_revenue'),
            'NET_INCOME_MIL': ('net_income_mil', 'net_income_currency', 'morningstar_annual_net_income'),
            'BOOK_VALUE_PER_SHARE': ('book_value_per_share', 'book_value_currency', 'morningstar_book_value_per_share'),
            'SHARE_MIL': ('share_mil', None, 'morningstar_share_outstanding'),
            'OPERATING_INCOME_MIL': ('operating_income_mil', 'operating_income_currency',
                                     'morningstar_annual_operating_income'),
            'GROSS_MARGIN': ('gross_margin', None, 'morningstar_annual_gross_margin'),
            'DIVIDENDS': ('dividends', 'dividend_currency', 'morningstar_annual_dividends'),
            'CURRENT_RATIO': ('current_ratio', None, 'morningstar_current_ratio'),
            'DEBT_TO_EQUITY': ('debt_to_equity', None, 'morningstar_debt_to_equity'),
        }
        has_updated = False
        for column in table_columns:
            if columns is None or column in columns:
                value_attr_name = table_columns.get(column)[0]
                currency_attr_name = table_columns.get(column)[1]
                table_name = table_columns.get(column)[2]
                date_values = getattr(financial, value_attr_name)
                currency = getattr(financial, currency_attr_name) if currency_attr_name is not None else None
                ret = self._update_date_values(stock, date_values, currency, version,
                                               table_name, column, overwrite)
                has_updated |= ret
        self._conn.commit()
        return has_updated

    # Update the revenue, net_income and other financial values with dates in the database
    # Return whether the row in database has been updated or not
    def _update_date_values(self, stock, date_values, currency, version, table_name, column_name, overwrite):
        if currency is not None:
            currency = currency.upper()
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
        sql_insert_currency = "INSERT INTO " + table_name + "(STOCK, DATE, VERSION, " + column_name + \
                              ", CURRENCY) VALUES('%s','%s','%s','%s', '%s')"
        sql_update = "UPDATE " + table_name + " SET "+column_name+" = '%s' WHERE STOCK = '%s' AND DATE = '%s' " \
                     " AND VERSION = '%s'"
        sql_update_currency = "UPDATE " + table_name + " SET " + column_name + " = '%s', " + \
                              " CURRENCY = '%s' WHERE STOCK = '%s' AND DATE = '%s' " + \
                              " AND VERSION = '%s'"
        has_updated = False
        for date in date_values:
            value = date_values[date]
            if date in existing_dates:
                if overwrite:
                    if currency is None:
                        cur.execute(sql_update % (value, stock, date, version))
                    else:
                        cur.execute(sql_update_currency % (value, currency, stock, date, version))
                    has_updated = True
            else:
                if currency is None:
                    cur.execute(sql_insert % (stock, date, version, value))
                else:
                    cur.execute(sql_insert_currency % (stock, date, version, value, currency))
                has_updated = True
        cur.close()
        return has_updated
