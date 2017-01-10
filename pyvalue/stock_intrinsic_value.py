# The valuation model for a stock
# Author: Liang Tang
# License: BSD
import numpy as np
import sys
from sklearn import linear_model

from pyvalue import constants
from pyvalue.morningstar import financial


class StockIntrinsicValue:
    def __init__(self):
        return

    @staticmethod
    def intrinsic_value(fin, ys=10, risk_free_rate=constants.US_10Y_NOTE_YIELD, log=None):
        """
        Compute the intrinsic value of a stock share
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param ys: the number of years for estimation
        :type ys: int
        :param risk_free_rate: the rate of US 10 years note (risk free 'ys' years return)
        :type risk_free_rate: float
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: the intrinsic value of a stock share
        """
        dividend = StockIntrinsicValue._predict_annual_dividend(fin, log)
        future_book_value = StockIntrinsicValue._predict_book_value(fin, 10, log)
        if future_book_value is None:
            return None
        iv = 0
        risk_free_ratio = (1 + risk_free_rate) ** ys
        iv += dividend * (1.0 - 1.0 / risk_free_ratio) / risk_free_rate
        iv += future_book_value / risk_free_ratio
        return iv

    @staticmethod
    def _predict_book_value(fin, num_yrs, log=None):
        """
        Compute the predicted book value after a number of years
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param num_yrs: the number of years
        :type num_yrs: int
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return: the predicted book value after 'num_yrs' years
        """
        n = len(fin.book_value_per_share)
        if n < 2:
            return None

        x_vals = np.array(range(n))
        x_vals.shape = (n, 1)
        book_values = fin.book_value_per_share
        sorted_dates = sorted(book_values.keys(), cmp=financial.cmp_date)
        y_vals = [book_values.get(date_str) for date_str in sorted_dates]

        # Create linear regression object
        regr = linear_model.LinearRegression()
        regr.fit(x_vals, y_vals)

        [predicted_y] = regr.predict(n + num_yrs)

        if log is not None:
            log.println("The historical book value for " + fin.stock)
            for date in sorted_dates:
                log.println("\t" + date + " : " + str(book_values.get(date)))
            log.println(
                "The predicted " + str(n) + " years book value per share of " + fin.stock + " : " + str(predicted_y))
        return predicted_y
        #
        #
        # # Get the last years's book value
        # sorted_dates = sorted(financial.book_value_per_share.keys(), cmp=morningstar_financials.cmp_date)
        # this_yr_val = financial.book_value_per_share[sorted_dates[-1]]
        # last_yr_val = financial.book_value_per_share[sorted_dates[-2]]
        # return last_yr_val + (last_yr_val - this_yr_val)*num_yrs

    @staticmethod
    def _predict_annual_dividend(fin, log=None):
        """
        Compute the predicted dividend (in dollar) per year in the next 10 years
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param log: the log information
        :type log: pyvalue.log_info.LogInfo
        :return:
        """
        if 'TTM' not in fin.dividends:
            predicted_dividend = 0
            if log is not None:
                log.println("No TTM in financial data for " + fin.stock
                            + ", the predicted dividend is 0")
        else:
            predicted_dividend = fin.dividends['TTM']
            if log is not None:
                log.println("the predicted dividend for " + fin.stock + " : " + str(predicted_dividend))
        return predicted_dividend
