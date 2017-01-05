# The valuation model for a stock
# Author: Liang Tang
# License: BSD
import numpy as np
from sklearn import linear_model

from pyvalue import constants
from pyvalue.morningstar import financial


class StockIntrinsicValue:

    def __init__(self):
        return

    @staticmethod
    def intrinsic_value(financial, ys=10, risk_free_rate=constants.US_10Y_NOTE_YIELD):
        """
        Compute the intrinsic value of a stock share
        :param financial: the morningstar financial object of the stock
        :type financial: financial.Financial
        :param ys: the number of years for estimation
        :type ys: int
        :param risk_free_rate: the rate of US 10 years note (risk free 'ys' years return)
        :type risk_free_rate: float
        :return: the intrinsic value of a stock share
        """
        dividend = StockIntrinsicValue.__predict_annual_dividend(financial)
        iv = 0
        risk_free_ratio = (1 + risk_free_rate) ** ys
        iv += dividend * (1.0 - 1.0/risk_free_ratio) / risk_free_rate
        future_book_value = StockIntrinsicValue.__predict_book_value(financial, 10)
        iv += future_book_value/risk_free_ratio
        return iv

    @staticmethod
    def __predict_book_value(fin, num_yrs):
        """
        Compute the predicted book value after a number of years
        :param financial: the morningstar financial object of the stock
        :type financial: financial.Financial
        :param num_yrs: the number of years
        :type num_yrs: int
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

        predicted_y = regr.predict(n+num_yrs)
        return predicted_y
        #
        #
        # # Get the last years's book value
        # sorted_dates = sorted(financial.book_value_per_share.keys(), cmp=morningstar_financials.cmp_date)
        # this_yr_val = financial.book_value_per_share[sorted_dates[-1]]
        # last_yr_val = financial.book_value_per_share[sorted_dates[-2]]
        # return last_yr_val + (last_yr_val - this_yr_val)*num_yrs

    @staticmethod
    def __predict_annual_dividend(financial):
        """
        Compute the predicted dividend (in dollar) per year in the next 10 years
        :param financial: the morningstar financial object of the stock
        :type financial: financial.Financial
        :return:
        """
        if 'TTM' not in financial.dividends:
            return 0
        else:
            return financial.dividends['TTM']


