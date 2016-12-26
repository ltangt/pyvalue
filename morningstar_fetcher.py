# Morningstar data fetcher
# Author: Liang Tang
# License: BSD
import urllib2
import StringIO
import os
import csv
import sys
import morningstar_financials


class MorningStarFetcherException(Exception):
    pass


class MorningStarFetcher:
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

    def fetch(self, stock, num_retries=3, use_cache=False):
        url = (r'http://financials.morningstar.com/ajax/exportKR2CSV.html?' +
               r'&callback=?&t={0}&region=usa&culture=en-US&cur=USD'.format(
                   stock))
        for try_idx in range(num_retries):
            try:
                filename = "tmp/" + stock + ".csv"
                if use_cache and self._has_cache(filename):
                    tmp_file = open(filename, "r")
                    html = tmp_file.read()
                    tmp_file.close()
                else:
                    response = urllib2.urlopen(url)
                    html = response.read()
                    if len(html.strip()) == 0:
                        raise MorningStarFetcherException("Empty response of the http request.")
                    tmp_file = open("tmp/"+stock + ".csv", "w")
                    tmp_file.write(html)
                    tmp_file.close()
                financial = morningstar_financials.MorningStarFinancial(stock)
                self._parse_html(html, financial)
                return financial
            except (MorningStarFetcherException, urllib2.HTTPError) as err:
                print stock + " : " + err.message + " in the "+str((try_idx+1))+" time"
                if try_idx == num_retries - 1:
                    sys.stderr.write('Failed to retrieve information for '+stock+'\n')

    def _has_cache(self, filename):
        if not os.path.isfile(filename):
            return False
        tmp_file = open(filename, "r")
        content = tmp_file.read()
        tmp_file.close()
        return len(content) > 0

    def _parse_html(self, html, financial):
        lines = html.split("\n")
        self._parse_financial(lines, financial)
        self._parse_liquidity(lines, financial)

    # Parse the financial section from the csv
    def _parse_financial(self, lines, financial):
        line_idx = self._find_line_index(lines, self.FINANCIAL_SECTION_HEADER)
        if line_idx == -1:
            raise MorningStarFetcherException("The html contains no " + self.FINANCIAL_SECTION_HEADER)
        # Get the section of lines
        sec_lines = MorningStarFetcher._get_section_lines(lines, line_idx)
        line_dates = lines[line_idx+1]
        # Get the dates
        dates = MorningStarFetcher._get_dates(line_dates)

        # Get the financial values
        financial.revenue_mil, financial.revenue_currency = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.REVENUE_LINE_PREFIX,
                                                           required_unit="mil")

        financial.net_income_mil, financial.net_income_currency = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.NET_INCOME_LINE_PREFIX,
                                                           required_unit="mil")

        financial.book_value_per_share, financial.book_value_currency = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.BOOK_VALUE_PER_SHARE_PREFIX,
                                                           has_currency=True, has_unit=False)

        financial.share_mil = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.SHARE_MIL_PREFIX,
                                                           has_currency=False, has_unit=False)

        financial.operating_income_mil, financial.operating_income_currency = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.OPERATING_INCOME_PREFIX,
                                                           required_unit="mil")

        gross_margin = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.GROSS_MARGIN,
                                                           has_currency=False, has_unit=False)
        # change the percentage number into real numbers
        financial.gross_margin = dict((date, value/100.0) for date, value in gross_margin.items())

        financial.dividends, financial.dividend_currency = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.DIVIDENDS,
                                                           has_currency=True, has_unit=False)

    # Parse the financial health section from the csv
    def _parse_liquidity(self, lines, financial):
        line_idx = self._find_line_index(lines, self.LIQUIDITY_SECTION_HEADER)
        if line_idx == -1:
            raise MorningStarFetcherException("The html contains no " + self.FINANCIAL_HEALTH_SECTION_HEADER)
        # Get the section of lines
        sec_lines = MorningStarFetcher._get_section_lines(lines, line_idx)
        line_dates = lines[line_idx]
        # Get the dates
        dates = MorningStarFetcher._get_dates(line_dates)
        # Get the financial values
        financial.current_ratio = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.CURRENT_RATIO_PREFIX,
                                                           has_currency=False, has_unit=False)

        financial.debt_to_equity = \
            MorningStarFetcher._parse_financial_with_dates(sec_lines, dates, self.DEBT_EQUITY_PREFIX,
                                                           has_currency=False, has_unit=False)

    @staticmethod
    def _parse_financial_with_dates(lines, dates, line_prefix,
                                    has_currency=True, has_unit=True, required_unit="mil"):
        values = {}
        line_idx = MorningStarFetcher._find_line_startwith(lines, line_prefix)
        # Get the currency and unit
        if line_idx == -1:
            raise MorningStarFetcherException("Cannot find line starting with" + line_prefix)
        line = lines[line_idx]
        line_postfix = line[len(line_prefix):] # the line by cutting the prefix part
        currency, unit = MorningStarFetcher._get_currency_and_unit(line_postfix, has_currency, has_unit)
        tokens = MorningStarFetcher._parse_csv_line(line)
        for i in range(1, len(tokens)):
            token = tokens[i].replace(',', '').strip()
            if len(token) == 0:
                continue
            value = float(token)
            if has_unit:
                value = MorningStarFetcher._unit_convert(unit, value, required_unit)
            date = dates[i - 1]
            values[date] = value
        if not has_currency:
            return values
        else:
            return values, currency

    @staticmethod
    def _get_currency_and_unit(line, has_currency=True, has_unit=True):
        if (not has_currency) and (not has_unit):
            return MorningStarFetcher.NO_CURRENCY, MorningStarFetcher.NO_UNIT
        line = line.replace("*", " ")
        line = line.strip()
        tokens_by_comma = line.split(",")
        if len(tokens_by_comma) == 0:
            raise MorningStarFetcherException("The line is empty : "+line)
        tokens = tokens_by_comma[0].split()
        tokens = [val.strip().lower() for val in tokens]
        if len(tokens) == 0:
            raise MorningStarFetcherException("The line has no currency or unit : "+line)
        elif len(tokens) == 1:
            if has_currency and (not has_unit):
                return tokens[-1], MorningStarFetcher.NO_UNIT
            elif (not has_currency) and has_unit:
                return MorningStarFetcher.NO_CURRENCY, tokens[-1]
            else:
                raise MorningStarFetcherException("The line only has currency or unit : "+line)
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
        if src_unit == "mil" and dest_unit == MorningStarFetcher.NO_UNIT:
            return src_value*(1000.0*1000.0)
        raise MorningStarFetcherException("Does not support to convert " + str(src_value) + " into "+dest_unit)

