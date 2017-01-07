# Morningstar fundamental data fetcher
# Author: Liang Tang
# License: BSD
import StringIO
import csv
import os
import sys
import urllib2

from pyvalue.morningstar import fetcher_exception
from pyvalue.morningstar import financial


class FundamentalFetcher:
    FINANCIAL_SECTION_HEADER = "Financials"
    LIQUIDITY_SECTION_HEADER = "Liquidity/Financial Health"

    REVENUE_LINE_PREFIX = "Revenue"
    NET_INCOME_LINE_PREFIX = "Net Income"
    BOOK_VALUE_PER_SHARE_PREFIX = "Book Value Per Share"
    SHARE_MIL_PREFIX = "Shares Mil"
    OPERATING_INCOME_PREFIX = "Operating Income"
    GROSS_MARGIN = "Gross Margin"
    DIVIDENDS = "Dividends"

    CURRENT_RATIO_PREFIX = "Current Ratio"
    DEBT_EQUITY_PREFIX = "Debt/Equity"

    NO_UNIT = ""
    NO_CURRENCY = ""

    def __init__(self):
        return

    def fetch(self, fin, num_retries=3, use_cache=False):
        """
        Fetch the fundamental data of a security
        :param fin: the morningstar financial object of the stock
        :type fin: financial.Financial
        :param num_retries: the number of retries
        :type num_retries: int
        :param use_cache: whether to use cache if cache exists
        :type use_cache: bool
        :return: whether success or not
        """
        stock = fin.stock
        url = (r'http://financials.morningstar.com/ajax/exportKR2CSV.html?' +
               r'&callback=?&t={0}&region=usa&culture=en-US&cur=USD'.format(
                   stock))
        for try_idx in range(num_retries):
            try:
                filename = "/tmp/" + stock + ".csv"
                if use_cache and FundamentalFetcher._has_cache(filename):
                    tmp_file = open(filename, "r")
                    html = tmp_file.read()
                    tmp_file.close()
                else:
                    response = urllib2.urlopen(url)
                    html = response.read()
                    if len(html.strip()) == 0:
                        raise fetcher_exception.FetcherException("Empty response of the http request.")
                    tmp_file = open(filename, "w")
                    tmp_file.write(html)
                    tmp_file.close()
                self._parse_html(html, fin)
                return True
            except (fetcher_exception.FetcherException, urllib2.HTTPError) as err:
                print stock + " : " + err.message + " in the "+str((try_idx+1))+" time"
                if try_idx == num_retries - 1:
                    sys.stderr.write('Failed to retrieve information for '+stock+'\n')
                    return False

    @staticmethod
    def _has_cache(filename):
        if not os.path.isfile(filename):
            return False
        tmp_file = open(filename, "r")
        content = tmp_file.read()
        tmp_file.close()
        return len(content) > 0

    def _parse_html(self, html, fin):
        lines = html.split("\n")
        self._parse_financial(lines, fin)
        self._parse_liquidity(lines, fin)

    # Parse the financial section from the csv
    def _parse_financial(self, lines, fin):
        line_idx = self._find_line_index(lines, self.FINANCIAL_SECTION_HEADER)
        if line_idx == -1:
            raise fetcher_exception.FetcherException("The html contains no " + self.FINANCIAL_SECTION_HEADER)
        # Get the section of lines
        sec_lines = FundamentalFetcher._get_section_lines(lines, line_idx)
        line_dates = lines[line_idx+1]
        # Get the dates
        dates = FundamentalFetcher._get_dates(line_dates)

        # Get the financial values
        fin.revenue_mil, financial.revenue_currency = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.REVENUE_LINE_PREFIX,
                                                           required_unit="mil")

        fin.net_income_mil, financial.net_income_currency = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.NET_INCOME_LINE_PREFIX,
                                                           required_unit="mil")

        fin.book_value_per_share, financial.book_value_currency = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.BOOK_VALUE_PER_SHARE_PREFIX,
                                                           has_currency=True, has_unit=False)

        fin.share_mil = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.SHARE_MIL_PREFIX,
                                                           has_currency=False, has_unit=False)

        fin.operating_income_mil, financial.operating_income_currency = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.OPERATING_INCOME_PREFIX,
                                                           required_unit="mil")

        gross_margin = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.GROSS_MARGIN,
                                                           has_currency=False, has_unit=False)
        # change the percentage number into real numbers
        fin.gross_margin = dict((date, value/100.0) for date, value in gross_margin.items())

        fin.dividends, fin.dividend_currency = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.DIVIDENDS,
                                                           has_currency=True, has_unit=False)

    # Parse the financial health section from the csv
    def _parse_liquidity(self, lines, fin):
        line_idx = self._find_line_index(lines, self.LIQUIDITY_SECTION_HEADER)
        if line_idx == -1:
            raise fetcher_exception.FetcherException("The html contains no " + self.FINANCIAL_HEALTH_SECTION_HEADER)
        # Get the section of lines
        sec_lines = FundamentalFetcher._get_section_lines(lines, line_idx)
        line_dates = lines[line_idx]
        # Get the dates
        dates = FundamentalFetcher._get_dates(line_dates)
        # Get the financial values
        fin.current_ratio = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.CURRENT_RATIO_PREFIX,
                                                           has_currency=False, has_unit=False)

        fin.debt_to_equity = \
            FundamentalFetcher._parse_financial_with_dates(sec_lines, dates, self.DEBT_EQUITY_PREFIX,
                                                           has_currency=False, has_unit=False)

    @staticmethod
    def _parse_financial_with_dates(lines, dates, line_prefix,
                                    has_currency=True, has_unit=True, required_unit="mil"):
        values = {}
        line_idx = FundamentalFetcher._find_line_startwith(lines, line_prefix)
        # Get the currency and unit
        if line_idx == -1:
            raise fetcher_exception.FetcherException("Cannot find line starting with" + line_prefix)
        line = lines[line_idx]
        line_postfix = line[len(line_prefix):] # the line by cutting the prefix part
        currency, unit = FundamentalFetcher._get_currency_and_unit(line_postfix, has_currency, has_unit)
        tokens = FundamentalFetcher._parse_csv_line(line)
        for i in range(1, len(tokens)):
            token = tokens[i].replace(',', '').strip()
            if len(token) == 0:
                continue
            value = float(token)
            if has_unit:
                value = FundamentalFetcher._unit_convert(unit, value, required_unit)
            date = dates[i - 1]
            values[date] = value
        if not has_currency:
            return values
        else:
            return values, currency

    @staticmethod
    def _get_currency_and_unit(line, has_currency=True, has_unit=True):
        if (not has_currency) and (not has_unit):
            return FundamentalFetcher.NO_CURRENCY, FundamentalFetcher.NO_UNIT
        line = line.replace("*", " ")
        line = line.strip()
        tokens_by_comma = line.split(",")
        if len(tokens_by_comma) == 0:
            raise fetcher_exception.FetcherException("The line is empty : " + line)
        tokens = tokens_by_comma[0].split()
        tokens = [val.strip().lower() for val in tokens]
        if len(tokens) == 0:
            raise fetcher_exception.FetcherException("The line has no currency or unit : " + line)
        elif len(tokens) == 1:
            if has_currency and (not has_unit):
                return tokens[-1], FundamentalFetcher.NO_UNIT
            elif (not has_currency) and has_unit:
                return FundamentalFetcher.NO_CURRENCY, tokens[-1]
            else:
                raise fetcher_exception.FetcherException("The line only has currency or unit : " + line)
        else:
            return tokens[-2], tokens[-1]

    @staticmethod
    def _find_line_index(lines, head):
        index = 0
        head = head.lower()
        for line in lines:
            line = line.lower()
            if head in line:
                return index
            index += 1
        return -1

    @staticmethod
    def _find_line_startwith(lines, start_with):
        index = 0
        for line in lines:
            if line.startswith(start_with):
                return index
            index += 1
        return -1

    @staticmethod
    def _get_dates(line):
        tokens = line.split(",")
        # Skip the first token, which is empty
        dates = []
        for i in range(1, len(tokens)):
            dates.append(tokens[i].strip())
        return dates

    @staticmethod
    def _parse_csv_line(line):
        f = StringIO.StringIO(line)
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            return row
        return None

    @staticmethod
    def _get_section_lines(lines, start_idx):
        section_lines = []
        idx = start_idx
        while idx < len(lines):
            if len(lines[idx].strip()) == 0:  # empty line
                break
            section_lines.append(lines[idx])
            idx += 1
        return section_lines

    @staticmethod
    def _unit_convert(src_unit, src_value, dest_unit):
        if src_unit == dest_unit:
            return src_value
        if src_unit == "" and dest_unit == "mil":
            return src_value/(1000.0*1000.0)
        if src_unit == "mil" and dest_unit == FundamentalFetcher.NO_UNIT:
            return src_value*(1000.0*1000.0)
        raise fetcher_exception.FetcherException("Does not support to convert " + str(src_value) + " into " + dest_unit)

