# symbol is token/coin
# run in a terminal like "py oop_main.py demo"

import psycopg2
import procedure_fncs
from oop_classes import *
import sorting_fncs
import oop_fncs

if __name__ == '__main__':

    program_version = procedure_fncs.command_line_interface()

    bitcoin = Token('BTCUSDT')
    print(f'Текущий курс Bitcoin: {float(bitcoin.get_price_now()):.4f} $')

    all_symbols = [Token(symbol_name) for symbol_name in procedure_fncs.get_all_symbols_from_exchange_information(program_version)]
    symbols_statistics = [(symbol, symbol.get_symbol_price_change_percent_for_week()) for symbol in all_symbols]
    sorting_fncs.toni_hoar_sort(symbols_statistics)

    top3_symbol_growth, top3_symbol_decline = procedure_fncs.get_tops3_symbol_change_price(symbols_statistics)
    oop_fncs.print_tops3_symbol_change_price(top3_symbol_growth, top3_symbol_decline)

    # sql_code(query, data) - хочется сделать что-то такое

    host_str = 'localhost'
    db_port = 5432
    db_str = 'test_db'
    u_name_str = 'postgres'
    db_password_str = '1'

    conn = psycopg2.connect(host=host_str, port=db_port, dbname=db_str,
                            user=u_name_str, password=db_password_str)  # подключение к БД
    cur = conn.cursor()  # курсор, нужен для выполнения SQL-команд в БД

    sql_query_str_1 = '''
        CREATE TABLE top3_symbols (
            token_name VARCHAR,
            open_price_week_ago NUMERIC,
            open_price_today NUMERIC,
            percent_price_difference NUMERIC,
            diffrence_type VARCHAR,
            load_timestamp TIMESTAMP
        )
    '''
    cur.execute(sql_query_str_1)

    sql_query_str_2 = '''
        INSERT INTO top3_symbols(
            token_name,
            open_price_week_ago,
            open_price_today,
            percent_price_difference,
            diffrence_type,
            load_timestamp
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    for symbol_object, percent_price_difference in tuple(top3_symbol_growth.items()) + tuple(top3_symbol_decline.items()):

        data = (symbol_object.symbol,
                symbol_object.get_open_price_a_week_ago(),
                symbol_object.get_open_price_today(),
                percent_price_difference,
                symbol_object.get_percent_price_difference_type(),
                symbol_object.load_utc_datetime
                )

        cur.execute(sql_query_str_2, data)

    conn.commit()

    cur.close()
    conn.close()
