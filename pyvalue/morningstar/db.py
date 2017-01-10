# Morningstar database interface
# Author: Liang Tang
# License: BSD
import pymysql

from pyvalue.morningstar import financial
from pyvalue import config


class Database:
    DB_NAME = "investment"

    # The key is the column name, the value is a tuple of value attribute, currency attribute, and the table name
    FUNDAMENTAL_TABLE_COLUMNS = {
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
    STOCK_PRICE_TABLE_COLUMNS = {
        'CLOSE_PRICE': ('stock_daily_close_price', 'stock_daily_price_currency', 'morningstar_stock_price'),
        'OPEN_PRICE': ('stock_daily_open_price', None, 'morningstar_stock_price'),
        'HIGHEST_PRICE': ('stock_daily_highest_price', None, 'morningstar_stock_price'),
        'LOWEST_PRICE': ('stock_daily_lowest_price', None, 'morningstar_stock_price'),
    }

    def __init__(self):
        config.init()
        self._db_server = config.config.get("mysql", "server").strip()
        self._db_port = int(config.config.get("mysql", "port").strip())
        self._db_username = config.config.get("mysql", "username").strip()
        self._db_password = config.config.get("mysql", "password").strip()
        self._conn = None

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

    def update_fundamentals(self, fin, version='1', columns=None, overwrite=True):
        """
        Update or insert the financial data into the database
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param version:
        :param columns:
        :param overwrite:
        :return:
        """
        stock = fin.stock

        has_updated = False
        for column in Database.FUNDAMENTAL_TABLE_COLUMNS:
            if columns is None or column in columns:
                value_attr_name = Database.FUNDAMENTAL_TABLE_COLUMNS.get(column)[0]
                currency_attr_name = Database.FUNDAMENTAL_TABLE_COLUMNS.get(column)[1]
                table_name = Database.FUNDAMENTAL_TABLE_COLUMNS.get(column)[2]
                date_values = getattr(fin, value_attr_name)
                currency = getattr(fin, currency_attr_name) if currency_attr_name is not None else None
                ret = self._update_single_column(stock, date_values, currency, version,
                                                 table_name, column, overwrite)
                has_updated |= ret
        self._conn.commit()
        return has_updated

    def update_stock_prices(self, fin, version='1', overwrite=True):
        """
        Update or insert the financial data into the database
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param version:
        :param overwrite:
        :return:
        """
        stock = fin.stock
        has_updated = False
        for column in Database.STOCK_PRICE_TABLE_COLUMNS:
            value_attr_name = Database.STOCK_PRICE_TABLE_COLUMNS.get(column)[0]
            currency_attr_name = Database.STOCK_PRICE_TABLE_COLUMNS.get(column)[1]
            table_name = Database.STOCK_PRICE_TABLE_COLUMNS.get(column)[2]
            date_values = getattr(fin, value_attr_name)
            currency = getattr(fin, currency_attr_name) if currency_attr_name is not None else None
            ret = self._update_single_column(stock, date_values, currency, version,
                                             table_name, column, overwrite)
            has_updated |= ret
        self._conn.commit()
        return has_updated

    # Update the single column value, such as revenue, net_income and other financial values with dates in the database
    # Return whether the row in database has been updated or not
    def _update_single_column(self, stock, date_values, currency, version, table_name, column_name, overwrite):
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

    def retrieve_fundamentals(self, fin, version='1'):
        """
        Retrive the fundamentals for the stock
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param version:
        :return: Sucess or not
        """
        stock = fin.stock
        for column in self.FUNDAMENTAL_TABLE_COLUMNS:
            value_attr_name = self.FUNDAMENTAL_TABLE_COLUMNS.get(column)[0]
            currency_attr_name = self.FUNDAMENTAL_TABLE_COLUMNS.get(column)[1]
            table_name = self.FUNDAMENTAL_TABLE_COLUMNS.get(column)[2]
            has_currency = currency_attr_name is not None
            date_values, currency = self._retrieve_date_values(stock, table_name, column, has_currency, version)
            if len(date_values) > 0:
                setattr(fin, value_attr_name, date_values)
                if has_currency:
                    assert currency is not None
                    setattr(fin, currency_attr_name, currency)
        return True

    def retrieve_historical_prices(self, fin, version='1'):
        """
        Retrive the fundamentals for the stock
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param version:
        :return: Sucess or not
        """
        stock = fin.stock
        for column in self.STOCK_PRICE_TABLE_COLUMNS:
            value_attr_name = self.STOCK_PRICE_TABLE_COLUMNS.get(column)[0]
            currency_attr_name = self.STOCK_PRICE_TABLE_COLUMNS.get(column)[1]
            table_name = self.STOCK_PRICE_TABLE_COLUMNS.get(column)[2]
            has_currency = currency_attr_name is not None
            date_values, currency = self._retrieve_date_values(stock, table_name, column, has_currency, version)
            if len(date_values) > 0:
                setattr(fin, value_attr_name, date_values)
                if has_currency:
                    assert currency is not None
                    setattr(fin, currency_attr_name, currency)
        return True

    def _retrieve_date_values(self, stock, table_name, column_name, has_currency, version='1'):
        sql_select_currency = "SELECT DATE, " + column_name + ", CURRENCY " +\
                              " FROM " + table_name +\
                              " WHERE STOCK = '%s' AND VERSION = '%s'"
        sql_select = "SELECT DATE, " + column_name + \
                     " FROM " + table_name + \
                     " WHERE STOCK = '%s' AND VERSION = '%s'"
        cur = self._conn.cursor()
        if has_currency:
            cur.execute(sql_select_currency % (stock, version))
        else:
            cur.execute(sql_select % (stock, version))
        result = cur.fetchall()
        date_values = {}
        currency = None
        for row in result:
            date = row[0]
            value = float(row[1])
            if has_currency:
                currency = row[2]
            date_values[date] = value
        cur.close()
        return date_values, currency
