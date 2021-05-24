from binance.client import Client
import numpy as np
from time import sleep
from datetime import datetime
import csv

#   Main function for calculating Moving Average
def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas  # as a numpy array


api_key = # API KEY from Binance
api_secret = # API Secret from Binance

client = Client(api_key, api_secret)
closed_prices = []

while(1):
    #create the timestamp
    now = datetime.now()

    print('Requested')

    #Request kline
    klines = client.get_historical_klines('ETHUSDT', client.KLINE_INTERVAL_1MINUTE, '150 minutes ago UTC')

    for single_kline in klines:
        closed_prices.append(float(single_kline[4]))

    closed_prices_np = np.array(closed_prices, dtype=np)

    # Calculate MA for 7 25 99
    ma_7 = moving_average(closed_prices_np, 7)[-1]
    ma_25 = moving_average(closed_prices_np, 25)[-1]
    ma_99 = moving_average(closed_prices_np, 99)[-1]

    # Check for buy or sell and print in CSV file
    if float(klines[-1][4]) > ma_7 and float(klines[-1][4]) > ma_25 and float(klines[-1][4]) > ma_99:
        print('Sell')
        with open('Closed_prices_list.csv', 'a', newline='') as closed_price:
            writer = csv.writer(closed_price)
            writer.writerow([now, 'Sell'])

    elif float(klines[-1][4]) < ma_7 and float(klines[-1][4]) < ma_25 and float(klines[-1][4]) < ma_99:
        print('Buy')
        with open('Closed_prices_list.csv', 'a', newline='') as closed_price:
            writer = csv.writer(closed_price)
            writer.writerow([now, 'Buy'])


    sleep(10)