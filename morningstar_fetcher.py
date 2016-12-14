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

    # Parse the financial compnents from the csv
    def _parse_financial(self, lines, financial):
        line_idx = self._find_line_index(lines, self.FINANCIAL_HEADER)
        if line_idx == -1:
            raise MorningStarFetcherException("The html contains no " + self.FINANCIAL_HEADER)
        line_dates = lines[line_idx+1]
        # Get the dates
        dates = self._get_dates(line_dates)
        # Get the revenue per year
        revenues = {}
        revenue_line = lines[line_idx+2]

        tokens = self._parse_csv_line(revenue_line)
        for i in range(1, len(tokens)-2):
            token = tokens[i].replace(',', '').strip()
            if len(token) == 0:
                continue
            revenue_in_million = float(token)
            date = dates[i]
            revenues[date] = revenue_in_million
        # Set the revenues
        financial.revenue_in_millions = revenues

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
