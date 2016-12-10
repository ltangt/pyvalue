import urllib2
import StringIO
import csv
import morningstar_financials


class MorningStarFetcher:
    FINANCIAL_HEADER = "Financials"

    def __init__(self):
        return

    def fetch(self, stock):
        url = (r'http://financials.morningstar.com/ajax/exportKR2CSV.html?' +
               r'&callback=?&t={0}&region=usa&culture=en-US&cur=USD'.format(
                   stock))
        response = urllib2.urlopen(url)
        html = response.read()
        tmp_file = open(stock + ".csv", "w")
        tmp_file.write(html)
        tmp_file.close()
        financials = morningstar_financials.MorningStarFinancials(stock)
        self._parse_html(html, financials)
        return financials

    def _parse_html(self, html, financials):
        lines = html.split("\n")
        self._parse_financials(lines, financials)

    # Parse the financial compnents from the csv
    def _parse_financials(self, lines, financials):
        line_idx = self._find_line_index(lines, self.FINANCIAL_HEADER)
        if line_idx == -1:
            raise Exception("The html contains no " + self.FINANCIAL_HEADER)
        line_dates = lines[line_idx+1]
        # Get the dates
        dates = self._get_dates(line_dates)
        print dates
        # Get the revenue per year
        revenues = {}
        revenue_line = lines[line_idx+2]

        tokens = self._parse_csv_line(revenue_line)
        for i in range(1, len(tokens)-2):
            revenue_in_million = float(tokens[i].replace(',', ''))
            date = dates[i]
            revenues[date] = revenue_in_million
        # Set the revenues
        financials.revenue_in_millions = revenues

    def _find_line_index(self, lines, head):
        index = 0
        head = head.lower()
        for line in lines:
            line = line.lower()
            if head in line:
                return index
            index += 1
        return -1

    def _get_dates(self, line):
        tokens = line.split(",")
        # Skip the first token, which is empty
        dates = []
        for i in range(1, len(tokens)):
            dates.append(tokens[i].strip())
        return dates

    def _parse_csv_line(self, line):
        f = StringIO.StringIO(line)
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            return row
        return None
