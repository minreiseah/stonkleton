from math import ceil
import numpy as np
import logging

from yahooquery import Ticker

logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO)

def get_discount_rate_from_beta(beta):
    if beta < 0.8:
        return 1.05
    elif beta <= 1:
        return 1.06
    elif beta > 1.5:
        return 1.09
    beta = ceil((beta-1)*10)
    dr = 1.06 + beta * 0.005
    return round(dr*1000)/1000

class Stock:
    def __init__(self, ticker, year=10) -> None:
        self.ticker = ticker
        self.year = year
        ticker_info = Ticker(ticker)
        
        # Basic
        self.current_price = ticker_info.financial_data[ticker]['currentPrice']
        self.shares_outstanding = ticker_info.key_stats[ticker]['sharesOutstanding']

        try:
            self.beta = ticker_info.key_stats[ticker]['beta']
            self.discount_rate = get_discount_rate_from_beta(self.beta)
        except KeyError as err:
            self.beta = 'NaN'
            self.discount_rate = 1.09
            logging.info(f'{ticker} does not have beta')
        
    
        # Balance Sheet
        types = ['CashCashEquivalentsAndShortTermInvestments', 'CashAndCashEquivalents', 'TotalDebt']
        bs = ticker_info.get_financial_data(types, frequency='q', trailing=False)
        if type(bs) == str: # if company did NOT report balance sheet
            print(bs)
            logging.info(bs)

        # Forex
        self.forex = bs.iloc[-1]['currencyCode']

        ## Cash (Quarter)
        try:
            self.cash_and_STI = bs.iloc[-1]['CashCashEquivalentsAndShortTermInvestments']
        except Exception as err:
            self.cash_and_STI = bs.iloc[-1]['CashAndCashEquivalents']

        ## Total Debt (Quarter)
        try:
            self.total_debt = bs.iloc[-1]['TotalDebt'] # Last Q
        except KeyError as err:
            logging.info(f'{ticker} does not have debt or did not report it this last quarter.')
            self.total_debt = 0

        # Operating Cash Flow (TTM/Annual)
        cf = ticker_info.get_financial_data('OperatingCashFlow', frequency='a', trailing=True)
        if not cf['periodType'].str.contains('TTM').any():
            print(f'{ticker} does not have TTM operating cash flow. Using annual OCF...')
            logging.info(f'{ticker} does not have TTM operating cash flow. Using annual OCF...')
        self.operating_cash_flow = cf.iloc[-1]['OperatingCashFlow']

        # Convert Currency to USD
        if self.forex != 'USD':
            currency_quote = self.forex + 'USD=X'
            conversion_ratio = Ticker(currency_quote).summary_detail[currency_quote]['ask']
            self.cash_and_STI = self.cash_and_STI * conversion_ratio
            self.total_debt = self.total_debt * conversion_ratio
            self.operating_cash_flow = self.operating_cash_flow * conversion_ratio
    
        # Estimates
        self.five_year_growth = ticker_info.earnings_trend[ticker]['trend'][4]['growth'] + 1
        self.ten_year_growth = min(1.15, self.five_year_growth)
    
    def attributes(self):
        return self.__dict__.items()

    # Calculate present_value (projected cash flow / d_r)
    def get_discount_rate(self, year):
        return self.discount_rate**year
    
    def get_projected_cash_flow(self, year):
        if year == 1:
            return self.operating_cash_flow * self.five_year_growth
        elif year < 6:
            return self.five_year_growth * self.get_projected_cash_flow(year-1)
        else:
            return self.ten_year_growth * self.get_projected_cash_flow(year-1)
    
    def get_present_value(self, year):
        return (self.get_projected_cash_flow(year) / self.get_discount_rate(year))
    
    def sum_present_value(self):
        sum = 0
        for i in range(1, self.year+1):
            sum += self.get_present_value(i)
        return sum
    
    # Forecast IV
    def get_iv(self):
        return self.sum_present_value() / self.shares_outstanding
    
    def get_iv_with_cash(self): # iv + cash
        return self.get_iv() + (self.cash_and_STI / self.shares_outstanding)
    
    def get_iv_with_debt(self): # iv + cash - debt
        return self.get_iv_with_cash() - (self.total_debt / self.shares_outstanding)
    
    def final_discount(self):
        final_iv = self.get_iv_with_debt()
        return (final_iv - self.current_price) / final_iv