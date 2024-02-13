# run in the terminal like "py procedure_main.py demo"

from procedure_fncs import *
from time_fncs import *


if __name__ == '__main__':

    program_version = command_line_interface()

    btc_price = get_btc_price()
    if btc_price:
        print(f'Текущий курс Bitcoin: {float(btc_price):.4f} $')

    all_symbols = get_all_symbols_from_exchange_information(program_version)
    limit = 30  # limit = get_limit_as_days_month()

    all_symbol_prices_dict = {}
    needed_symbols_data_lst = []

    for symbol in all_symbols:

        all_open_prices_lst = get_klines(symbol, limit)

        if len(all_open_prices_lst) >= limit:

            today_week_month_prices_lst = [all_open_prices_lst[0], all_open_prices_lst[-8], all_open_prices_lst[-1]]

            open_price_a_week_ago, open_price_today = today_week_month_prices_lst[1], today_week_month_prices_lst[0]
            symbol_price_change_percent_for_week = get_price_chandge_percent_for_week(open_price_a_week_ago, open_price_today)

            data = [symbol, symbol_price_change_percent_for_week]
            data.extend(today_week_month_prices_lst)

            needed_symbols_data_lst.append(data)

            all_symbol_prices_dict[symbol] = all_open_prices_lst

    needed_symbols_data_lst.sort(key=lambda x: x[1])  # ? сортировка по возрастанию symbol_price_change_percent_for_week
    print_tops3_symbol_change_price(needed_symbols_data_lst)

    # дополнительно можно сделать custom_request
