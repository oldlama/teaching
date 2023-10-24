from fncs_btc import *


if __name__ == '__main__':

    btc_price = get_btc_price()
    if btc_price:
        print(f'Текущий курс Bitcoin: {float(btc_price):.4f} $')

    data = symbol_price_change_percent()
    top3 = get_top3_symbol_growth_and_decline(data)

    print_tops3_symbol_change_price(top3)
    print_std_deviations(top3)






