from fncs_btc import *


if __name__ == '__main__':

    symbol_price_change_percent_dict = {}
    all_symbols = get_all_symbols_from_exchange_information()

    for symbol in all_symbols:
        price_change_percent = get_rolling_window_price_change_statistics(symbol)
        symbol_price_change_percent_dict.setdefault(symbol, price_change_percent)

    symbol_price_change_percent_dict = {}

    with open('symbol_price_change_percent.json', 'w') as file:
        json.dump(symbol_price_change_percent_dict, file)
