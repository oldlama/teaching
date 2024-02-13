from procedure_main import all_symbol_prices_dict, needed_symbols_data_lst
import numpy as np
import pandas as pd

# топы за неделю, но их std за месяц, чтобы оценить насколько сильно за неделю произошло изменение цены,
# ориентируясь на величину month_std


def print_std_deviations(tops1_symbols_std):

    print('Сравнение стандартных отклонений по топ1:')
    df = pd.DataFrame.from_dict(tops1_symbols_std, orient='index', columns=['топ1 STD'])
    print(df)


top1_week_symbol_decline = needed_symbols_data_lst[0]['symbol']
top1_week_symbol_growth = needed_symbols_data_lst[-1]['symbol']

tops1_symbols_std = {
    top1_week_symbol_decline: np.std(all_symbol_prices_dict[top1_week_symbol_decline]) * 100,
    top1_week_symbol_growth: np.std(all_symbol_prices_dict[top1_week_symbol_growth]) * 100,
}

print_std_deviations(tops1_symbols_std)
