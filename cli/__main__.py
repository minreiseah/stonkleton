import pandas as pd
from prettytable import PrettyTable
import logging

from stock import Stock

def main():
    logging.basicConfig(filename='logfile.log', filemode='w', level=logging.DEBUG)
    while(True):
        event() 

def event():

    # get user input
    tickers = [x.upper() for x in input("Input Ticker(s): ").split()]
    tickers = [x.replace('.', '-') for x in tickers]
    print('Loading...')

    # used later to concantenate lists into df; then export to csv
    df_list = []

    # printing
    t = PrettyTable()
    t.field_names = ['Stock', 'Estimated Discount', 'Expected IV (USD)']
    t.align = 'r'
    t.align['Stock'] = 'l'

    for ticker in tickers:
        # Process ticker
        try:
            ticker_info = Stock(ticker)
        except Exception as err:
            logging.info(err)
            print(f'Error with {ticker}\n')
            continue
        
        # Ignore tickers with negative operating cash flow
        if ticker_info.operating_cash_flow < 0:
            discount = '-ve OPERATING CF'
            final_iv = '-ve OPERATING CF'
        # Format discount and final_iv data
        else:
            discount = "{:.2%}".format(ticker_info.final_discount())
            final_iv = "${:.2f}".format(ticker_info.get_iv_with_debt())
        t.add_row([ticker, discount, final_iv])

        # Prepare data to be added into csv of all data
        columns = [k for k,v in ticker_info.attributes()]
        columns.extend([
            'projected_cash_flow', 'discount_rate', 'present_value', 'sum_present_value',
            'initial_iv', 'iv_cash', 'iv_cash_debt_final', 'estimated discount'
        ])

        data = [v for k,v in ticker_info.attributes()]
        data.append(ticker_info.get_projected_cash_flow(ticker_info.year))
        data.append(ticker_info.get_discount_rate(ticker_info.year))
        data.append(ticker_info.get_present_value(ticker_info.year))
        data.append(ticker_info.sum_present_value())
        data.append(ticker_info.get_iv())
        data.append(ticker_info.get_iv_with_cash())
        data.append(ticker_info.get_iv_with_debt())
        data.append(ticker_info.final_discount())

        df = pd.DataFrame(data=[data], columns=columns)
        df_list.append(df)

        del ticker_info

    # Output data
    print(t)

    # Output full data csv
    try:
        df = pd.concat(df_list, ignore_index=True)
        df.to_csv('full_data.csv')
    except Exception as err:
        print('No valid tickers')

if __name__ == '__main__':
    main()