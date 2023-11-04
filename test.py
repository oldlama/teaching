import requests
import numpy as np
from exceptions import *
from datetime import datetime
import pandas as pd

def is_correct_response(response):

    flag = False

    try:
        if response.status_code != 200:
            raise GetRespStatusBut200Error()
    except GetRespStatusBut200Error:
        print(f'"{response}" status code other than 200.')
    else:
        flag = True

    return flag


def get_klines(symbol='BTCUSDT', interval='1d', limit=31):

    base_endpoint = 'https://api4.binance.com'

    kline_data_endpoint = base_endpoint + '/api/v3/klines'

    kline_data_parameters = {'symbol': symbol, 'interval': interval, 'limit': limit}
    kline_data_response = requests.get(kline_data_endpoint, params=kline_data_parameters)

    kline_data = None

    if is_correct_response(kline_data_response):
        kline_data = kline_data_response.json()

    return kline_data


def get_matrix_kline_data(kline_data_json):

    columns = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume',
               'Kline Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
               'Taker buy quote asset volume', 'Unused field, ignore']

    matrix_kline_data = pd.DataFrame(kline_data_json, columns=columns)

    dt_kline_open_times_lst = [convert_time(unix_time) for unix_time in
                               matrix_kline_data['Kline open time'].values]
    matrix_kline_data['Kline open time'] = dt_kline_open_times_lst

    float_open_price_lst = [custom_round(float(price)) for price in matrix_kline_data['Open price'].values]
    matrix_kline_data['Open price'] = float_open_price_lst

    return matrix_kline_data


def convert_time(unix_time):

    _t = unix_time / 1000
    timestamp = datetime.utcfromtimestamp(_t)
    date = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return date


def custom_round(number):

    ndigits = {
        number >= 1000: 0,
        100 <= number < 1000: 1,
        1 <= number < 100: 2,
        0 <= number < 1: 4,
    }

    return round(number, ndigits[True])


kline_data_json = get_klines(symbol='BTCUSDT')

matrix_kline_data = get_matrix_kline_data(kline_data_json)

prices_data = [custom_round(float(price)) for price in matrix_kline_data['Open price']]

how_many_time_ago = 'month'

old_open_price = {
    'week': prices_data[-8],
    'month': prices_data[0]
}

new_open_price = prices_data[-1]
difference = ((new_open_price - old_open_price[how_many_time_ago])/new_open_price) * 100

print(f'{round(difference, 2)}%')


