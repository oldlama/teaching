# docs: https://binance-docs.github.io/apidocs/voptions/en/#general-info

import requests
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def print_btc_price():

    base_endpoint = 'https://api4.binance.com'  # 'https://api.binance.com' 'https://data-api.binance.vision'

    symbol_price_ticker_endpoint = base_endpoint + '/api/v3/ticker/price'
    symbol_price_ticker_parameter = {'symbol': 'BTCUSDT'}
    symbol_price_ticker_response = requests.get(symbol_price_ticker_endpoint, params=symbol_price_ticker_parameter)

    if symbol_price_ticker_response.status_code == 200:

        btc_price = symbol_price_ticker_response.json()['price']
        print(f'Текущий курс Bitcoin: {float(btc_price):.4f} $')

    else:
        print(f'Error {symbol_price_ticker_response.status_code} with symbol_price_ticker_response')


def print_tops3_symbol_change_price():

    top3 = get_top3_symbol_growth_and_decline()
    top3_symbol_growth, top3_symbol_decline = top3['growth'], top3['decline']

    df_growth = pd.DataFrame.from_dict(top3_symbol_growth, orient='index', columns=['прирост, %'])
    df_decline = pd.DataFrame.from_dict(top3_symbol_decline, orient='index', columns=['упадок, %'])

    print('Топ3 по наибольшему изменению стоимости в процентах за прошедшую неделю:')
    print(df_growth)
    print(df_decline)


def get_top3_symbol_growth_and_decline():

    with open('symbol_price_change_percent.json') as file:
        data = json.load(file)
        symbol_price_change_percent_lst = sorted(data.items(), key=lambda item: float(item[1]))

        top3_symbol_decline_dict = {key: value for key, value in symbol_price_change_percent_lst[:3]}
        top3_symbol_growth_dict = {key: value for key, value in symbol_price_change_percent_lst[:-4:-1]}

        symbol_growth_and_decline = {
            'growth': top3_symbol_growth_dict,
            'decline': top3_symbol_decline_dict,
        }

        return symbol_growth_and_decline


def print_std_deviations():

    top3 = get_top3_symbol_growth_and_decline()
    top1_symbol_growth, top1_symbol_decline = list(top3['growth'])[0], list(top3['decline'])[0]

    std_month_symbol_growth = percent_std_deviation(top1_symbol_growth, 'Open price', '1 month')
    std_week_symbol_growth = percent_std_deviation(top1_symbol_growth, 'Open price', '1 week')

    std_month_symbol_decline = percent_std_deviation(top1_symbol_decline, 'Open price', '1 month')
    std_week_symbol_decline = percent_std_deviation(top1_symbol_decline, 'Open price', '1 week')

    std_dev_data = {
        top1_symbol_growth: [std_week_symbol_growth, std_month_symbol_growth],
        top1_symbol_decline: [std_week_symbol_decline, std_month_symbol_decline],
    }

    row_indices = ['За неделю', 'За месяц']

    print('Сравнение стандартных отклонений по топ1:')
    print(pd.DataFrame(std_dev_data, index=row_indices))


def percent_std_deviation(symbol, feature, period):

    data = get_matrix_candlestick_data(symbol, period)

    return data[feature].std() * 100


def get_matrix_candlestick_data(symbol, period):

    base_endpoint = 'https://data-api.binance.vision'
    candlestick_data_endpoint = base_endpoint + '/api/v3/klines'

    endTime = get_server_timestamp()

    startTime = get_start_timestamp_for_server(endTime, how_many_time_ago=period)

    interval = '1d'
    limit = delta_days(end_timestamp=endTime/1000, start_timestamp=startTime/1000) + 1

    candlestick_data_parameters = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit,
        'endTime': endTime,
        'startTime': startTime,
    }

    candlestick_data_responce = requests.get(candlestick_data_endpoint, params=candlestick_data_parameters)

    columns = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Unused field, ignore']
    matrix_candlestick_data = pd.DataFrame(candlestick_data_responce.json(), columns=columns)

    dt_kline_open_times_lst = [convert_time(unix_time) for unix_time in matrix_candlestick_data['Kline open time'].values]
    matrix_candlestick_data['Kline open time'] = dt_kline_open_times_lst

    float_open_price_lst = [custom_round(float(price)) for price in matrix_candlestick_data['Open price'].values]
    matrix_candlestick_data['Open price'] = float_open_price_lst

    return matrix_candlestick_data


def get_server_timestamp():

    base_endpoint = 'https://data-api.binance.vision'
    server_time_endpoint = base_endpoint + '/api/v3/time'
    server_time_responce = requests.get(server_time_endpoint)

    return server_time_responce.json()['serverTime']  # текущая временная метка прямо сейчас в UTC, тип int (мкс - последние три цифры)


def get_start_timestamp_for_server(end_timestamp_for_server, how_many_time_ago):

    utc_timestamp = end_timestamp_for_server / 1000
    startTime_timestamp = some_time_ago_utc_timestamp(utc_timestamp, how_many_time_ago)

    return int(startTime_timestamp * 1000)  # временная метка ровно месяц назад в UTC для сервера


def some_time_ago_utc_timestamp(utc_timestamp, how_many_time_ago):

    dt = datetime.utcfromtimestamp(utc_timestamp)

    delta = {
        '1 month': relativedelta(months=1),
        '1 week': relativedelta(weeks=1),
    }

    datetime_some_time_ago = dt - delta[how_many_time_ago]

    return datetime_some_time_ago.timestamp()


def delta_days(start_timestamp, end_timestamp):

    end_datetime = datetime.utcfromtimestamp(end_timestamp)
    start_datetime = datetime.fromtimestamp(start_timestamp)

    return (end_datetime - start_datetime).days


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


def get_all_symbols_from_exchange_information():

    base_endpoint = 'https://data-api.binance.vision'  # 'https://api4.binance.com' 'https://api.binance.com' 'https://data-api.binance.vision'

    exchange_information_endpoint = base_endpoint + '/api/v3/exchangeInfo'
    exchange_information_response = requests.get(exchange_information_endpoint)

    all_symbols_lst = []

    if exchange_information_response.status_code == 200:
        for info in exchange_information_response.json()['symbols']:
            all_symbols_lst.append(info['symbol'])
    else:
        print(f'Error {exchange_information_response.status_code} with exchange_information_response')

    return all_symbols_lst


def get_rolling_window_price_change_statistics(symbol='ETHBTC', duration='7d'):

    base_endpoint = 'https://data-api.binance.vision'

    statistics_endpoint = base_endpoint + '/api/v3/ticker'

    statistics_parameters = {'symbol': symbol, 'windowSize': duration}
    statistics_response = requests.get(statistics_endpoint, params=statistics_parameters)

    price_change_percent = None

    if statistics_response.status_code == 200:
        price_change_percent = statistics_response.json()['priceChangePercent']
    else:
        print(f'Error {statistics_response.status_code} with statistics_response')

    return price_change_percent
