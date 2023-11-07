# docs: https://binance-docs.github.io/apidocs/voptions/en/#general-info

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from exceptions import *


def get_btc_price():

    base_endpoint = 'https://api4.binance.com'  # 'https://api.binance.com' 'https://data-api.binance.vision'

    symbol_price_ticker_endpoint = base_endpoint + '/api/v3/ticker/price'
    symbol_price_ticker_parameter = {'symbol': 'BTCUSDT'}
    symbol_price_ticker_response = requests.get(symbol_price_ticker_endpoint, params=symbol_price_ticker_parameter)

    btc_price = None

    if is_correct_response(symbol_price_ticker_response):
        btc_price = symbol_price_ticker_response.json()['price']

    return btc_price


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


def symbol_price_change_percent(period, run_program_variant):

    symbol_price_change_percent_dict = {}
    all_symbols = get_all_symbols_from_exchange_information()

    symbols = {
        'demo': all_symbols[:10],
        'work': all_symbols
    }

    for symbol in symbols[run_program_variant]:
        price_change_percent = get_price_chandge_percent(symbol, period)
        symbol_price_change_percent_dict.setdefault(symbol, price_change_percent)

    return symbol_price_change_percent_dict


def get_all_symbols_from_exchange_information(quote_asset='USDT'):

    base_endpoint = 'https://data-api.binance.vision'  # 'https://api4.binance.com' 'https://api.binance.com' 'https://data-api.binance.vision'

    exchange_information_endpoint = base_endpoint + '/api/v3/exchangeInfo'
    exchange_information_response = requests.get(exchange_information_endpoint)

    all_symbols_lst = []

    if is_correct_response(exchange_information_response):
        for info in exchange_information_response.json()['symbols']:
            if info['symbol'].endswith(quote_asset):
                all_symbols_lst.append(info['symbol'])

    return all_symbols_lst


def get_price_chandge_percent(symbol, period='1 week'):

    prices_data = get_prices_data(symbol)

    old_open_price = {
        '1 week': prices_data[-8],
        '1 month': prices_data[0]
    }

    new_open_price = prices_data[-1]

    if new_open_price == old_open_price[period]:
        percent_difference = 0
    elif old_open_price[period] != 0:
        percent_difference = ((new_open_price / old_open_price[period]) - 1) * 100
    else:
        percent_difference = 100

    return round(percent_difference, 2)


def get_prices_data(symbol='BTCUSDT'):

    matrix_kline_data = get_matrix_kline_data(symbol)

    prices_data = [custom_round(float(price)) for price in matrix_kline_data['Open price']]

    return prices_data


def get_matrix_kline_data(symbol):

    kline_data_json = get_klines(symbol)
    matrix_kline_data = None

    if kline_data_json:
        columns = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Unused field, ignore']
        matrix_kline_data = pd.DataFrame(kline_data_json, columns=columns)

        dt_kline_open_times_lst = [convert_time(unix_time) for unix_time in matrix_kline_data['Kline open time'].values]
        matrix_kline_data['Kline open time'] = dt_kline_open_times_lst

        float_open_price_lst = [custom_round(float(price)) for price in matrix_kline_data['Open price'].values]
        matrix_kline_data['Open price'] = float_open_price_lst

    return matrix_kline_data


def get_klines(symbol='BTCUSDT'):

    base_endpoint = 'https://data-api.binance.vision'
    kline_data_endpoint = base_endpoint + '/api/v3/klines'

    kline_data_parameters = {
        'symbol': symbol,
        'interval': '1d',
        'limit': get_limit_as_days_month(),
    }

    kline_data_responce = requests.get(kline_data_endpoint, params=kline_data_parameters)

    kline_data = None

    if is_correct_response(kline_data_responce):
        kline_data = kline_data_responce.json()

    return kline_data


def get_limit_as_days_month():

    endTime = get_server_timestamp()
    startTime = get_start_timestamp_for_server(endTime)

    limit = delta_days(end_timestamp=endTime/1000, start_timestamp=startTime/1000) + 1

    return limit


def get_server_timestamp():

    base_endpoint = 'https://data-api.binance.vision'
    server_time_endpoint = base_endpoint + '/api/v3/time'
    server_time_responce = requests.get(server_time_endpoint)

    return server_time_responce.json()['serverTime']  # текущая временная метка прямо сейчас в UTC, тип int (мкс - последние три цифры)


def get_start_timestamp_for_server(end_timestamp_for_server):

    utc_timestamp = end_timestamp_for_server / 1000
    startTime_timestamp = month_ago_utc_timestamp(utc_timestamp)

    return int(startTime_timestamp * 1000)  # временная метка ровно месяц назад в UTC для сервера


def delta_days(start_timestamp, end_timestamp):

    end_datetime = datetime.utcfromtimestamp(end_timestamp)
    start_datetime = datetime.fromtimestamp(start_timestamp)

    return (end_datetime - start_datetime).days


def month_ago_utc_timestamp(utc_timestamp):

    dt = datetime.utcfromtimestamp(utc_timestamp)

    datetime_month_time_ago = dt - relativedelta(months=1)

    return datetime_month_time_ago.timestamp()


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


def get_top3_symbol_growth_and_decline(data):

    symbol_price_change_percent_lst = sorted(data.items(), key=lambda item: float(item[1]))

    top3_symbol_decline_dict = {key: value for key, value in symbol_price_change_percent_lst[:3]}
    top3_symbol_growth_dict = {key: value for key, value in symbol_price_change_percent_lst[:-4:-1]}

    symbol_growth_and_decline = {
        'growth': top3_symbol_growth_dict,
        'decline': top3_symbol_decline_dict,
    }

    return symbol_growth_and_decline


def print_tops3_symbol_change_price(top3):

    top3_symbol_growth, top3_symbol_decline = top3['growth'], top3['decline']

    df_growth = pd.DataFrame.from_dict(top3_symbol_growth, orient='index', columns=['прирост, %'])
    df_decline = pd.DataFrame.from_dict(top3_symbol_decline, orient='index', columns=['упадок, %'])

    print('Топ3 по наибольшему изменению стоимости в процентах за прошедшую неделю:')
    print(df_growth)
    print(df_decline)


def print_std_deviations(top3):

    top1_symbol_growth, top1_symbol_decline = list(top3['growth'])[0], list(top3['decline'])[0]

    std_month_symbol_growth = percent_std_deviation(top1_symbol_growth, '1 month')
    std_week_symbol_growth = percent_std_deviation(top1_symbol_growth, '1 week')

    std_month_symbol_decline = percent_std_deviation(top1_symbol_decline, '1 month')
    std_week_symbol_decline = percent_std_deviation(top1_symbol_decline, '1 week')

    std_dev_data = {
        top1_symbol_growth: [std_week_symbol_growth, std_month_symbol_growth],
        top1_symbol_decline: [std_week_symbol_decline, std_month_symbol_decline],
    }

    row_indices = ['За неделю', 'За месяц']

    print('Сравнение стандартных отклонений по топ1:')
    print(pd.DataFrame(std_dev_data, index=row_indices))


def percent_std_deviation(symbol, period):

    prices_data = get_prices_data(symbol)

    data = {
        '1 week': prices_data[-8:],
        '1 month': prices_data
    }

    return np.std(data[period]) * 100
