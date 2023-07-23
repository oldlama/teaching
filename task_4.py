from task_4_funcs import *

flag = True

if 'привет' in input().lower() and flag:

    print('Привет!')

    user_request = input(f'Вот, что я могу:\n'
                         f'НАОРАТЬ\nПодсчитать символы\n'
                         f'Заменить\nCписок слов\nВыход\n'
                         f'Введите требуемое действие или вызовите оператора:\n')

    menu = {
        'наорать': up_print,
        'подсчитать символы': letters_count_print,
        'заменить': symbol_change_print,
        'список слов': words_from_string_print,
    }

    while flag:
        in_menu_condition = user_request.lower() in menu
        is_operator_condition = 'оператор' in user_request.lower()

        if user_request.lower() == 'выход':
            flag = False
        elif is_operator_condition:
            print('Зову оператора!')
            flag = False
        elif in_menu_condition:
            menu[user_request.lower()](input('Введите строку: '))
            user_request = input(f'Вот, что я могу:\n'
                                 f'НАОРАТЬ\nПодсчитать символы\n'
                                 f'Заменить\nCписок слов\nВыход\n'
                                 f'Введите требуемое действие или вызовите оператора:\n')
        else:
            user_request = input(f'Вот, что я могу:\n'
                                 f'НАОРАТЬ\nПодсчитать символы\n'
                                 f'Заменить\nCписок слов\nВыход\n'
                                 f'Введите требуемое действие или вызовите оператора:\n')
