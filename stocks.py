'''
TODO LIST:
= buy/sell stocks
= live monitor
= check monitor
'''

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

stocksList = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list').json()

stocks_symbols = []
current_stock_price = {}
stock_closing_prices = {}

day1Reading = []
day2Reading = []
day3Reading = []
day4Reading = []
day5Reading = []
day6Reading = []
currentReading = []

# pprint(stocksList)
for stock in stocksList['symbolsList']:
    stocks_symbols.append(stock['symbol'])
    if ('name' not in stock.keys() or stock['name'] == ""):
        current_stock_price[stock['symbol']] = stock["price"]
    else:
        stock_name = stock['symbol'] + ": " + stock['name']
        current_stock_price[stock_name] = stock["price"]
# pprint(stocks_prices)
stock_count = 1
# for stock in stocks_symbols[:20]:
for stock in stocks_symbols:
    # print(stock)
    print(f"Iterating through Stock {stock_count} out of {len(current_stock_price.items())}!")
    stock_data = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}').json()
    if 'historical' in stock_data:
        for data in stock_data['historical'][-7:]:
            datetime_obj = datetime.strptime(data['date'], '%Y-%m-%d').strftime('%m-%d-%Y')
            stock_closing_prices[datetime_obj] = data['close']
    else:
        stock_closing_prices["Stock has no ""historical data""!"] = 'Closing Price: NaN'

    # print(stock, list(stock_closing_prices.items())[0:7])

    day1Reading.append(list(stock_closing_prices.values())[0])
    day2Reading.append(list(stock_closing_prices.values())[1])
    day3Reading.append(list(stock_closing_prices.values())[2])
    day4Reading.append(list(stock_closing_prices.values())[3])
    day5Reading.append(list(stock_closing_prices.values())[4])
    day6Reading.append(list(stock_closing_prices.values())[5])
    currentReading.append(list(stock_closing_prices.values())[6])
    # if (
    #         "Stock has no ""historical data""!" not in stock_closing_prices or 'Closing Price: NaN' not in stock_closing_prices):
    #     plt.plot(list(stock_closing_prices.keys()), list(stock_closing_prices.values()), color=np.random.rand(3, ),
    #              label=stock)
    stock_count += 1

    '''plt.plot(list(stock_closing_prices.keys())[0:7], list(stock_closing_prices.values())[0:7], color = np.random.rand(3, ), label=stock)
    plt.title(f'Price of {stock} in USD from {list(stock_closing_prices.keys())[0]} to {list(stock_closing_prices.keys())[6]}')
    plt.xticks(rotation=45)
    plt.legend(loc='center right')
    plt.savefig(f'C:/Users/username/Documents/Stocks/{stock}_stock.png', bbox_inches='tight')
    # plt.show()
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
# plt.legend(loc='best')
# plt.show()'''

dataframe_dict = {"Stock": stocks_symbols,
                  f"CP Recording: {list(stock_closing_prices.keys())[0]}": day1Reading,
                  f"Day 2 CP Recording: {list(stock_closing_prices.keys())[1]}": day2Reading,
                  f"Day 3 CP Recording: {list(stock_closing_prices.keys())[2]}": day3Reading,
                  f"Day 4 CP Recording: {list(stock_closing_prices.keys())[3]}": day4Reading,
                  f"Day 5 CP Recording: {list(stock_closing_prices.keys())[4]}": day5Reading,
                  f"Day 6 CP Recording: {list(stock_closing_prices.keys())[5]}": day6Reading,
                  f"Today's CP Recording: {list(stock_closing_prices.keys())[6]}": currentReading}
dataframe = pd.DataFrame(dataframe_dict)

dataframe = dataframe.style.applymap(color_negative_red)

pd.set_option('display.max_rows', len(stocks_symbols))
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 1)

print('\n')
dataframe.to_csv('C:/Users/username/Documents/Stocks/stocks_data.csv')
print("Finished exporting Pandas DataFrame to a CSV File")
dataframe.to_excel('C:/Users/username/Documents/Stocks/stocks_data.xlsx', sheet_name=f"From {list(stock_closing_prices.keys())[0]} to {list(stock_closing_prices.keys())[6]}")
print("Finished exporting Pandas DataFrame to an Excel Spreadsheet")
print('\n')

# print(dataframe)
dataframe.head(10)