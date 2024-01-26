from fncs import *
from time_fncs import *
import argparse
import numpy as np


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('run', choices=['demo', 'work'])
    args = parser.parse_args()

    btc_price = get_btc_price()
    if btc_price:
        print(f'Текущий курс Bitcoin: {float(btc_price):.4f} $')

    all_symbols = get_all_symbols_from_exchange_information()
    limit = 30

    if args.run == 'demo':
        all_symbols = all_symbols[:10]
    elif args.run == 'work':
        # limit = get_limit_as_days_month()
        pass

    all_symbol_prices_dict = {}
    needed_symbols_data_lst = []

    for symbol in all_symbols:

        all_open_prices_lst = get_klines(symbol, limit)

        if len(all_open_prices_lst) >= limit:
            all_symbol_prices_dict[symbol] = all_open_prices_lst
            today_week_month_prices_lst = [all_open_prices_lst[0], all_open_prices_lst[-8], all_open_prices_lst[-1]]

            old_open_price = today_week_month_prices_lst[1]  # open_price a week ago
            new_open_price = today_week_month_prices_lst[0]  # open_price today
            symbol_price_change_percent_for_week = get_price_chandge_percent_for_week(old_open_price, new_open_price)

            data = [symbol, symbol_price_change_percent_for_week]
            data.extend(today_week_month_prices_lst)

            needed_symbols_data_lst.append(data)

    needed_symbols_data_lst.sort(key=lambda x: x[1])
    keys = ['symbol', 'symbol_price_change_percent_for_week', 'open_price_today', 'open_price_week_ago', 'open_price_month_ago']
    needed_symbols_data_lst = [dict(zip(keys, values)) for values in needed_symbols_data_lst]

    top1_week_symbol_decline = needed_symbols_data_lst[0]['symbol']
    top1_week_symbol_growth = needed_symbols_data_lst[-1]['symbol']

    # топы за неделю, но их std за месяц, чтобы оценить насколько сильно за неделю произошло изменение цены,
    # ориентируясь на величину month_std

    tops1_symbols_std = {
        top1_week_symbol_decline: np.std(all_symbol_prices_dict[top1_week_symbol_decline]) * 100,
        top1_week_symbol_growth: np.std(all_symbol_prices_dict[top1_week_symbol_growth]) * 100,
    }

    top3_symbol_decline = {data['symbol']: data['symbol_price_change_percent_for_week'] for data in needed_symbols_data_lst[:3]}
    top3_symbol_growth = {data['symbol']: data['symbol_price_change_percent_for_week'] for data in needed_symbols_data_lst[:-4:-1]}

    print_tops3_symbol_change_price(top3_symbol_decline, top3_symbol_growth)
    print_std_deviations(tops1_symbols_std)

    # дополнительно можно сделать custom_request
    #asdsadsad тут изменили