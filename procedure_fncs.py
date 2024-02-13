# docs: https://binance-docs.github.io/apidocs/voptions/en/#general-info

import argparse
import requests
import pandas as pd
from exceptions import *


def command_line_interface():

    parser = argparse.ArgumentParser()
    parser.add_argument('run', choices=['demo', 'work'])
    args = parser.parse_args()

    return args.run


def get_btc_price():

    base_endpoint = 'https://data-api.binance.vision'  # 'https://api4.binance.com'  # 'https://api.binance.com' 'https://data-api.binance.vision'

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


def get_all_symbols_from_exchange_information(program_version, quote_asset='USDT'):

    base_endpoint = 'https://data-api.binance.vision'  # 'https://api4.binance.com' 'https://api.binance.com' 'https://data-api.binance.vision'

    exchange_information_endpoint = base_endpoint + '/api/v3/exchangeInfo'
    exchange_information_response = requests.get(exchange_information_endpoint)

    all_symbols_lst = []

    if is_correct_response(exchange_information_response):
        for info in exchange_information_response.json()['symbols']:
            if info['symbol'].endswith(quote_asset):
                all_symbols_lst.append(info['symbol'])

    if program_version == 'demo':
        all_symbols_lst = all_symbols_lst[:10]
    elif program_version == 'work':
        pass

    return all_symbols_lst


def get_klines(symbol, limit):

    base_endpoint = 'https://data-api.binance.vision'
    kline_data_endpoint = base_endpoint + '/api/v3/klines'

    kline_data_parameters = {
        'symbol': symbol,
        'interval': '1d',
        'limit': limit,
    }

    kline_data_responce = requests.get(kline_data_endpoint, params=kline_data_parameters)
    all_open_prices_lst = []

    if is_correct_response(kline_data_responce):

        kline_data_lst_json = kline_data_responce.json()
        all_open_prices_lst = [custom_round(float(data[1])) for data in kline_data_lst_json]

    return all_open_prices_lst


def custom_round(number):

    ndigits = {
        number >= 1000: 0,
        100 <= number < 1000: 1,
        1 <= number < 100: 2,
        0 <= number < 1: 4,
    }

    return round(number, ndigits[True])


def get_price_chandge_percent_for_week(old_open_price, new_open_price):

    if new_open_price == old_open_price:
        percent_difference = 0
    elif float(old_open_price) != 0.0:
        #percent_difference = ((float(new_open_price) / float(old_open_price)) - 1) * 100
        percent_difference = ((float(new_open_price) - float(old_open_price)) / float(old_open_price)) * 100
        #print(percent_difference)
    else:
        percent_difference = 100

    return round(percent_difference, 2)


def get_tops3_symbol_change_price(needed_symbols_data_lst):
    keys = ['symbol',
            'symbol_price_change_percent_for_week']  # , 'open_price_today', 'open_price_week_ago', 'open_price_month_ago']
    needed_symbols_data_lst = [dict(zip(keys, values)) for values in needed_symbols_data_lst]

    # топы за неделю, но их std за месяц, чтобы оценить насколько сильно за неделю произошло изменение цены,
    # ориентируясь на величину month_std

    decline_dicts_lst, growth_dicts_lst = needed_symbols_data_lst[:3], needed_symbols_data_lst[:-4:-1]
    top3_symbol_decline, top3_symbol_growth = {}, {}

    for decline in decline_dicts_lst:
        key, value = decline['symbol'], decline['symbol_price_change_percent_for_week']
        top3_symbol_decline[key] = value if value < 0 else 'нет упадка'

    for growth in growth_dicts_lst:
        key, value = growth['symbol'], growth['symbol_price_change_percent_for_week']
        top3_symbol_growth[key] = value if value > 0 else 'нет прироста'

    return top3_symbol_growth, top3_symbol_decline


def print_tops3_symbol_change_price(top3_symbol_growth, top3_symbol_decline):

    df_growth = pd.DataFrame.from_dict(top3_symbol_growth, orient='index', columns=['прирост, %'])
    df_decline = pd.DataFrame.from_dict(top3_symbol_decline, orient='index', columns=['упадок, %'])

    print('Топ3 по наибольшему изменению стоимости в процентах за прошедшую неделю:')
    print(df_growth)
    print(df_decline)
