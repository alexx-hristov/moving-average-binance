from binance.client import Client
from time import sleep
import numpy as np
import mysql.connector
from datetime import datetime

#   Main function for calculating Moving Average
def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas  # as a numpy array

api_key = # API Key from Binance
api_secret = # API Secret from Binance

client = Client(api_key, api_secret)
closed_prices = []


print('Init')
while (1):
    #create the timestamp
    now = datetime.now()

    # Connect to MySQL
    db = mysql.connector.connect(
        host='localhost',
        user='bot',
        password='',
        database='python'
    )

    cursor = db.cursor()
    sql = ('INSERT INTO test_python1 (time, action) VALUES (%s, %s)')

    print('Request')
    #Request kline
    klines = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, '150 minutes ago UTC')

    for single_kleine in klines:
        closed_prices.append(float(single_kleine[4]))

    closed_prices_np = np.asarray(closed_prices, dtype=np)

    # Calculate MA for 7 25 99
    ma_7 = moving_average(closed_prices, 7)[-1]
    ma_25 = moving_average(closed_prices, 25)[-1]
    ma_99 = moving_average(closed_prices, 99)[-1]

    # Check for buy or sell and updating the DB
    if float(klines[-1][4]) < ma_7 and float(klines[-1][4]) < ma_25 and float(klines[-1][4]) < ma_99:
        print('Sell', now)

        sell_signal = now, 'Sell'
        cursor.execute(sql, sell_signal)

        db.commit()

    elif float(klines[-1][4]) > ma_7 and float(klines[-1][4]) > ma_25 and float(klines[-1][4]) > ma_99:
        print('Buy', now)
        buy_signal = now, 'Buy'
        cursor.execute(sql, buy_signal)

        db.commit()

    else:
        print('Do nothing')

    sleep(10)