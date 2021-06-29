from math import ceil
from decimal import *
from yahooquery import Ticker
import logging



def get_discount_rate_from_beta(beta):
    getcontext().prec = 1
    if beta < 0.8:
        return 0.05
    elif beta <= 1:
        return 0.06
    beta = ceil((beta-1)*10)
    dr = 0.06 + beta * 0.005
    return round(dr*1000)/1000

class Stock:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        ticker_info = Ticker(ticker)
        
        # Basic
        self.current_price = ticker_info.financial_data[ticker]['currentPrice']
        self.shares_outstanding = ticker_info.key_stats[ticker]['sharesOutstanding'] #? floatShares
        try:
            self.beta = ticker_info.key_stats[ticker]['beta']
        except KeyError as err:
            self.beta = 2
            print(f'{ticker} does not have beta')
        self.discount_rate = get_discount_rate_from_beta(self.beta) + 1
        

        # Financials
        types = ['CashCashEquivalentsAndShortTermInvestments', 'OperatingCashFlow', 'TotalDebt']
        afd = ticker_info.get_financial_data(types, frequency='q', trailing=True)

        self.cash_and_STI = afd.iloc[-2]['CashCashEquivalentsAndShortTermInvestments'] # Last Q
        self.operating_cash_flow = afd.iloc[-1]['OperatingCashFlow'] # TTM
        try:
            self.total_debt = afd.iloc[-2]['TotalDebt'] # Last Q
        except KeyError as err:
            print(f'{ticker} does not have net debt')
            self.total_debt = 0
    
        # Estimates
        self.five_year_growth = ticker_info.earnings_trend[ticker]['trend'][4]['growth'] + 1
        self.ten_year_growth = min(0.15, self.five_year_growth) + 1
    
    def attributes(self):
        return self.__dict__.items()

    def get_discount_rate(self, year=10):
        return self.discount_rate**year
    
    def get_projected_cash_flow(self, year=10):
        if year == 1:
            return self.operating_cash_flow * self.five_year_growth
        elif year < 6:
            return self.five_year_growth * self.get_projected_cash_flow(year-1)
        else:
            return self.ten_year_growth * self.get_projected_cash_flow(year-1)
    
    def get_present_value(self, year=10):
        return (self.get_projected_cash_flow(year) / self.get_discount_rate(year))
    
    def sum_present_value(self, year=10):
        sum = 0
        for i in range(1, year+1):
            sum += self.get_present_value(i)
        return sum

    def get_iv(self, year=10):
        return self.sum_present_value(year) / self.shares_outstanding
    
    def get_iv_with_cash(self, year=10): # iv + cash
        return self.get_iv(year) + (self.cash_and_STI / self.shares_outstanding)
    
    def get_iv_with_debt(self, year=10): # iv + cash - debt
        return self.get_iv_with_cash(year) - (self.total_debt / self.shares_outstanding)
    
    def discount_to_price(self, year=10):
        final_iv = self.get_iv_with_debt(year)
        return (final_iv - self.current_price) / final_iv

stock = Stock("RBLX")
for k, v in stock.attributes():
    print(k, '=', v)

print(stock.discount_to_price())