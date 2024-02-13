import requests
from procedure_fncs import is_correct_response, custom_round
from time_fncs import get_server_timestamp
from datetime import datetime

class Token:

    BASE_ENDPOINT = 'https://data-api.binance.vision'
    LIMIT_AS_DAYS_MONTH = 30  # limit = get_limit_as_days_month(), from time_fncs import *
    UTC_SERVER_TIMESTAMP = get_server_timestamp() / 1000

    def __init__(self, symbol):
        self.symbol = symbol
        self.base_endpoint = Token.BASE_ENDPOINT
        self.symbol_price_ticker_endpoint = Token.BASE_ENDPOINT + '/api/v3/ticker/price'
        self.kline_data_endpoint = Token.BASE_ENDPOINT + '/api/v3/klines'
        self.klines = Token.get_klines(self, Token.LIMIT_AS_DAYS_MONTH)
        self.load_utc_datetime = datetime.utcfromtimestamp(Token.UTC_SERVER_TIMESTAMP)

        if len(self.klines) < Token.LIMIT_AS_DAYS_MONTH:
            raise ValueError('Свечи должны быть хотя бы за последние 30 дней.')  # сделать try-except, где используется class Token

    def __str__(self):
        return f'Token: {self.symbol}'

    def get_price_now(self):

        symbol_price_ticker_parameter = {'symbol': self.symbol}
        symbol_price_ticker_response = requests.get(self.symbol_price_ticker_endpoint, params=symbol_price_ticker_parameter)

        btc_price = None

        if is_correct_response(symbol_price_ticker_response):
            btc_price = symbol_price_ticker_response.json()['price']

        return btc_price

    def get_klines(self, limit):

        kline_data_parameters = {
            'symbol': self.symbol,
            'interval': '1d',
            'limit': limit,
        }

        kline_data_response = requests.get(self.kline_data_endpoint, params=kline_data_parameters)
        all_open_prices_lst = []

        if is_correct_response(kline_data_response):
            kline_data_lst_json = kline_data_response.json()
            all_open_prices_lst = [custom_round(float(data[1])) for data in kline_data_lst_json]

        return all_open_prices_lst

    def get_open_price_a_week_ago(self):
        return self.klines[-8]

    def get_open_price_today(self):
        return self.klines[0]

    def get_open_price_a_month_ago(self):
        return self.klines[-1]

    def get_symbol_price_change_percent_for_week(self):

        old_open_price = self.get_open_price_a_week_ago()
        new_open_price = self.get_open_price_today()

        if new_open_price == old_open_price:
            percent_difference = 0
        elif float(old_open_price) != 0.0:
            percent_difference = ((float(new_open_price) - float(old_open_price)) / float(old_open_price)) * 100
        else:
            percent_difference = 100

        return round(percent_difference, 2)

    def get_percent_price_difference_type(self):

        percent_price_difference = self.get_symbol_price_change_percent_for_week()
        percent_price_difference_type = 'стабильность'

        if percent_price_difference > 0:
            percent_price_difference_type = 'прирост'
        elif percent_price_difference < 0:
            percent_price_difference_type = 'упадок'

        return percent_price_difference_type

    def print(self):
        print(f"{self.symbol}: {self.get_symbol_price_change_percent_for_week()} %")
