# The valuation model for a stock
# Author: Liang Tang
# License: BSD
import morningstar_financials


def cmp_date(date1, date2):
    """
    Compare two date strings, which are the keys of the financial date values
    :param date1:
    :type date1: str
    :param date2:
    :type date2: str
    :return:
    """
    if date1 == date2:
        return 0
    elif date1 == 'TTM':
        return 1
    elif date2 == 'TTM':
        return -1
    else:
        date1 = date1.replace("-", "")
        date2 = date2.replace("-", "")
        return int(date1) - int(date2)


class StockValuation:

    def __init__(self):
        return

    @staticmethod
    def intrinsic_value(financial, us_10yr_rate):
        """
        Compute the intrinsic value of a stock share
        :param financial: the morningstar financial object of the stock
        :type financial: morningstar_financials.MorningStarFinancial
        :param us_10yr_rate: the rate of US 10 years note (risk free 10 years return)
        :type us_10yr_rate: float
        :return: the intrinsic value of a stock share
        """
        dividend = StockValuation.predict_annual_dividend(financial)
        ys = 10
        iv = 0
        iv += dividend * (1.0 - (1+us_10yr_rate)**ys)/us_10yr_rate if dividend is not None else 0
        book_value = StockValuation.predict_book_value(financial, 10)
        iv += book_value/((1+us_10yr_rate)**ys)
        return iv

    @staticmethod
    def predict_book_value(financial, num_yrs):
        """
        Compute the predicted book value after a number of years
        :param financial: the morningstar financial object of the stock
        :type financial: morningstar_financials.MorningStarFinancial
        :param num_yrs: the number of years
        :type num_yrs: int
        :return: the predicted book value after 'num_yrs' years
        """
        if len(financial.book_value_per_share) < 2:
            return None
        # Get the last years's book value
        sorted_dates = sorted(financial.book_value_per_share.keys(), cmp=cmp_date)
        this_yr_val = financial.book_value_per_share[sorted_dates[-1]]
        last_yr_val = financial.book_value_per_share[sorted_dates[-2]]
        return last_yr_val + (last_yr_val - this_yr_val)*num_yrs

    @staticmethod
    def predict_annual_dividend(financial):
        """
        Compute the predicted dividend (in dollar) per year in the next 10 years
        :param financial: the morningstar financial object of the stock
        :type financial: morningstar_financials.MorningStarFinancial
        :return:
        """
        if 'TTM' not in financial:
            return None
        else:
            return financial.dividends['TTM']


