# Morningstar data fetcher
# Author: Liang Tang
# License: BSD
import urllib2
import StringIO
import csv
import morningstar_financials


class MorningStarFetcherException(Exception):
    pass


class MorningStarFetcher:
    FINANCIAL_HEADER = "Financials"
    REVENUE_LINE_PREFIX = "Revenue USD Mil"
    NET_INCOME_LINE_PREFIX = "Net Income USD Mil"
    BOOK_VALUE_PER_SHARE = "Book Value Per Share"

    def __init__(self):
        return

    def fetch(self, stock, num_retries = 3):
        url = (r'http://financials.morningstar.com/ajax/exportKR2CSV.html?' +
               r'&callback=?&t={0}&region=usa&culture=en-US&cur=USD'.format(
                   stock))
        for try_idx in range(num_retries):
            try:
                response = urllib2.urlopen(url)
                html = response.read()
                if len(html.strip()) == 0:
                    raise MorningStarFetcherException("Empty result")
                tmp_file = open("tmp/"+stock + ".csv", "w")
                tmp_file.write(html)
                tmp_file.close()
                financial = morningstar_financials.MorningStarFinancial(stock)
                self._parse_html(html, financial)
                return financial
            except MorningStarFetcherException:
                pass

    def _parse_html(self, html, financial):
        lines = html.split("\n")
        self._parse_financial(lines, financial)

    # Parse the financial components from the csv
    def _parse_financial(self, lines, financial):
        line_idx = self._find_line_index(lines, self.FINANCIAL_HEADER)
        if line_idx == -1:
            raise MorningStarFetcherException("The html contains no " + self.FINANCIAL_HEADER)
        line_dates = lines[line_idx+1]
        # Get the dates
        dates = self._get_dates(line_dates)

        # Get the financial values
        financial.revenue_in_millions = \
            MorningStarFetcher._parse_financial_with_dates(lines, dates, self.REVENUE_LINE_PREFIX)

        financial.net_income_in_millions = \
            MorningStarFetcher._parse_financial_with_dates(lines, dates, self.NET_INCOME_LINE_PREFIX)

        financial.book_value_per_share = \
            MorningStarFetcher._parse_financial_with_dates(lines, dates, self.BOOK_VALUE_PER_SHARE)

    @staticmethod
    def _parse_financial_with_dates(lines, dates, line_prefix):
        values = {}
        line_idx = MorningStarFetcher._find_line_startwith(lines, line_prefix)
        if line_idx == -1:
            raise MorningStarFetcherException("Cannot find "+line_prefix+ " line.")
        line = lines[line_idx]
        tokens = MorningStarFetcher._parse_csv_line(line)
        for i in range(1, len(tokens)-2):
            token = tokens[i].replace(',', '').strip()
            if len(token) == 0:
                continue
            value = float(token)
            date = dates[i]
            values[date] = value
        return values

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
