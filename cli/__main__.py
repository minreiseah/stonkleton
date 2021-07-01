from stock import Stock

import pandas as pd
from prettytable import PrettyTable
import logging

def main():
    logging.basicConfig(filename='logfile.log', filemode='w', level=logging.DEBUG)
    done = True
    while(True):
        if(done):
            event()

def event():

    done = False

    # get user input
    tickers = [x.upper() for x in input("Input Ticker(s): ").split()]
    tickers = [x.replace('.', '-') for x in tickers]
    print('Loading...')

    # used later to concantenate lists into df; then export to csv
    df_list = []

    # printint
    t = PrettyTable()
    t.field_names = ['Stock', 'Estimated Discount', 'Expected IV (USD)']
    t.align = 'r'
    t.align['Stock'] = 'l'


    for ticker in tickers:
        try:
            ticker_info = Stock(ticker)
        except Exception as err:
            logging.info(err)
            print(f'Error with {ticker}\n')
            continue
        
        if ticker_info.operating_cash_flow < 0:
            discount = '-ve OPERATING CF'
            final_iv = '-ve OPERATING CF'
        else:
            discount = "{:.2%}".format(ticker_info.final_discount())
            final_iv = "${:.2f}".format(ticker_info.get_iv_with_debt())
        t.add_row([ticker, discount, final_iv])

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

        # for k, v in zip(columns, data):
        #     print(k, '=', v)

        del ticker_info

    print(t)

    try:
        df = pd.concat(df_list, ignore_index=True)
        df.to_csv('full_data.csv')
    except:
        print('No valid tickers')
    
    done = True

if __name__ == '__main__':
    main()