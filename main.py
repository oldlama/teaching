from fncs import *
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('run', choices=['demo', 'work'])
    args = parser.parse_args()

    btc_price = get_btc_price()
    if btc_price:
        print(f'Текущий курс Bitcoin: {float(btc_price):.4f} $')

    data = symbol_price_change_percent('1 week', args.run)
    top3 = get_top3_symbol_growth_and_decline(data)

    print_tops3_symbol_change_price(top3)
    print_std_deviations(top3)
