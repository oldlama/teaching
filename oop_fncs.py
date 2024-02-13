def print_tops3_symbol_change_price(top3_symbol_growth, top3_symbol_decline):

    print('Топ3 по наибольшему изменению стоимости в процентах за прошедшую неделю:')

    print('прирост---------')
    for symbol in top3_symbol_growth:
        symbol.print()

    print('упадок---------')
    for symbol in top3_symbol_decline:
        symbol.print()
