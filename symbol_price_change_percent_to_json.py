import requests
import json

def get_all_symbols_from_exchange_information():

    base_endpoint = 'https://data-api.binance.vision'  # 'https://api4.binance.com' 'https://api.binance.com' 'https://data-api.binance.vision'

    exchange_information_endpoint = base_endpoint + '/api/v3/exchangeInfo'
    exchange_information_response = requests.get(exchange_information_endpoint)

    all_symbols_lst = []
    quote_asset = 'USDT'
    i = 0
    if exchange_information_response.status_code == 200:
        for info in exchange_information_response.json()['symbols']:
            if info['symbol'].endswith(quote_asset):
                all_symbols_lst.append(info['symbol'])
    else:
        print(f'Error {exchange_information_response.status_code} with exchange_information_response')

    return all_symbols_lst


def get_rolling_window_price_change_statistics(symbol='BTCUSDT', duration='7d'):

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


if __name__ == '__main__':

    symbol_price_change_percent_dict = {}
    all_symbols = get_all_symbols_from_exchange_information()

    for symbol in all_symbols:
        price_change_percent = get_rolling_window_price_change_statistics(symbol)
        symbol_price_change_percent_dict.setdefault(symbol, price_change_percent)

    with open('symbol_price_change_percent.json', 'w') as file:
        json.dump(symbol_price_change_percent_dict, file)
