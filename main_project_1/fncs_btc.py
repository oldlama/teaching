# docs: https://binance-docs.github.io/apidocs/voptions/en/#general-info

import requests

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


