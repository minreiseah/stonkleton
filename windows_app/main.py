from stock import Stock
import pandas as pd
import logging

logging.basicConfig(filename='logfile.log', filemode='w', level=logging.DEBUG)

tickers = [x.upper() for x in input("Tickers: ").split()]
tickers = [x.replace('.', '-') for x in tickers]

df_list = []

print('Stock | Discounts | Expected IV')

for ticker in tickers:
    try:
        ticker_info = Stock(ticker)
    except Exception as err:
        logging.info(err)
        print(f'Error with {ticker}')
        continue

    discount = "{:.5%}".format(ticker_info.final_discount())
    final_iv = "${:.2f}".format(ticker_info.get_iv_with_debt())
    print(f'{"helo": < 16} gello')

    ticker_info.get_projected_cash_flow()
    ticker_info.get_discount_rate()
    ticker_info.get_present_value()
    ticker_info.get_iv()
    ticker_info.get_iv_with_cash()
    ticker_info.get_iv_with_debt()


    columns = [k for k,v in ticker_info.attributes()]
    data = [[v for k,v in ticker_info.attributes()]]
    df = pd.DataFrame(data=data, columns=columns)
    df_list.append(df)

df = pd.concat(df_list, ignore_index=True)
df.to_csv('full_data.csv')