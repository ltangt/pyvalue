# Global constants used by this project
# Author: Liang Tang
# License: BSD
import os
import sys
import csv

SP500_2015_10 = [
    'A', 'AA', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABT', 'ACE', 'ACN', 'ADBE',
    'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'ADT', 'AEE', 'AEP', 'AES', 'AET',
    'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AKAM', 'ALL', 'ALLE', 'ALTR', 'ALXN',
    'AMAT', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANTM', 'AON',
    'APA', 'APC', 'APD', 'APH', 'ARG', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AXP',
    'AZO', 'BA', 'BAC', 'BAX', 'BBBY', 'BBT', 'BBY', 'BCR', 'BDX', 'BEN',
    'BF.B', 'BHI', 'BIIB', 'BK', 'BLK', 'BLL', 'BMY', 'BRCM', 'BRK.B', 'BSX',
    'BWA', 'BXLT', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAM', 'CAT', 'CB', 'CBG',
    'CBS', 'CCE', 'CCI', 'CCL', 'CELG', 'CERN', 'CF', 'CHK', 'CHRW', 'CI',
    'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CMCSK', 'CME', 'CMG', 'CMI', 'CMS',
    'CNP', 'CNX', 'COF', 'COG', 'COH', 'COL', 'COP', 'COST', 'CPB', 'CPGX',
    'CRM', 'CSC', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVC', 'CVS',
    'CVX', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS',
    'DISCA', 'DISCK', 'DLPH', 'DLTR', 'DNB', 'DO', 'DOV', 'DOW', 'DPS', 'DRI',
    'DTE', 'DUK', 'DVA', 'DVN', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL',
    'EMC', 'EMN', 'EMR', 'ENDP', 'EOG', 'EQIX', 'EQR', 'EQT', 'ES', 'ESRX',
    'ESS', 'ESV', 'ETFC', 'ETN', 'ETR', 'EW', 'EXC', 'EXPD', 'EXPE', 'F',
    'FAST', 'FB', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLIR',
    'FLR', 'FLS', 'FMC', 'FOSL', 'FOX', 'FOXA', 'FSLR', 'FTI', 'FTR', 'GAS',
    'GD', 'GE', 'GGP', 'GILD', 'GIS', 'GLW', 'GM', 'GMCR', 'GME', 'GNW', 'GOOG',
    'GOOGL', 'GPC', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAR', 'HAS',
    'HBAN', 'HBI', 'HCA', 'HCBK', 'HCN', 'HCP', 'HD', 'HES', 'HIG', 'HOG',
    'HON', 'HOT', 'HP', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM',
    'IBM', 'ICE', 'IFF', 'INTC', 'INTU', 'IP', 'IPG', 'IR', 'IRM', 'ISRG',
    'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY',
    'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KSS', 'KSU',
    'L', 'LB', 'LEG', 'LEN', 'LH', 'LLL', 'LLTC', 'LLY', 'LM', 'LMT', 'LNC',
    'LOW', 'LRCX', 'LUK', 'LUV', 'LVLT', 'LYB', 'M', 'MA', 'MAC', 'MAR', 'MAS',
    'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MHFI', 'MHK',
    'MJN', 'MKC', 'MLM', 'MMC', 'MMM', 'MNK', 'MNST', 'MO', 'MON', 'MOS', 'MPC',
    'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTB', 'MU', 'MUR', 'MYL', 'NAVI', 'NBL',
    'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NLSN', 'NOC', 'NOV',
    'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O',
    'OI', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PBI', 'PCAR',
    'PCG', 'PCL', 'PCLN', 'PCP', 'PDCO', 'PEG', 'PEP', 'PFE', 'PFG', 'PG',
    'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG',
    'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'PYPL',
    'QCOM', 'QRVO', 'R', 'RAI', 'RCL', 'REGN', 'RF', 'RHI', 'RHT', 'RIG', 'RL',
    'ROK', 'ROP', 'ROST', 'RRC', 'RSG', 'RTN', 'SBUX', 'SCG', 'SCHW', 'SE',
    'SEE', 'SHW', 'SIAL', 'SIG', 'SJM', 'SLB', 'SLG', 'SNA', 'SNDK', 'SNI',
    'SO', 'SPG', 'SPLS', 'SRCL', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ',
    'SWK', 'SWKS', 'SWN', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDC', 'TE', 'TEL',
    'TGNA', 'TGT', 'THC', 'TIF', 'TJX', 'TMK', 'TMO', 'TRIP', 'TROW', 'TRV',
    'TSCO', 'TSN', 'TSO', 'TSS', 'TWC', 'TWX', 'TXN', 'TXT', 'TYC', 'UA', 'UAL',
    'UHS', 'UNH', 'UNM', 'UNP', 'UPS', 'URBN', 'URI', 'USB', 'UTX', 'V', 'VAR',
    'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ',
    'WAT', 'WBA', 'WDC', 'WEC', 'WFC', 'WFM', 'WHR', 'WM', 'WMB', 'WMT', 'WRK',
    'WU', 'WY', 'WYN', 'WYNN', 'XEC', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX',
    'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']

US_10Y_NOTE_YIELD = 0.02543

SP500_2016 = None


def get_sp_500_companies():
    global SP500_2016
    if SP500_2016 is not None:
        return SP500_2016
    SP500_2016 = []
    package_dir = os.path.dirname(__file__)
    sp500_file_path = package_dir + "/../sp500.csv"
    sp500_file = open(sp500_file_path, "rb")
    reader = csv.reader(sp500_file, delimiter=',')
    next(reader)  # skip the header
    for row in reader:
        SP500_2016.append(row[0])
    sp500_file.close()
    return SP500_2016


def get_sp_500_universe():
    universe = get_sp_500_companies()
    universe.append("SPY")
    return universe


def get_nasaq_efts_symbols():
    """
    Get the Nasaq traded EFT symbols
    :return:
    """
    package_dir = os.path.dirname(__file__)
    file_path = package_dir + "/../nasdaqtraded.txt"
    file = open(file_path, "rb")
    reader = csv.reader(file, delimiter='|')
    next(reader)  # skip the header
    efts = []
    for row in reader:
        is_eft = row[5]
        if is_eft == 'Y':
            efts.append(row[1])
    file.close()
    return efts
