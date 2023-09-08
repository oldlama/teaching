from random import randint, choice
from string import printable
from typing import List
from task_6_exceptions import *
import pickle


def is_try_menu_variants(user_choice: str) -> bool:

    flag = False

    try:
        if not (int(user_choice) == 1 or int(user_choice) == 2):
            raise StartWayError()

    except StartWayError:
        print('Выбранный номер действия для начала программы за рамками предложенных вариантов.')
    except ValueError:
        print('Это не номер пункта.')

    else:
        flag = True

    return flag


def list_filtering() -> List[list]:

    list_of_lists = generate_list_of_lists()
    max_num_of_scroll = len(list_of_lists)
    num_of_scroll = input('Ведите номер списка: ')
    user_chosen_list_and_sorted_list = []

    if is_try_correct_entered_num_of_scroll(num_of_scroll, max_num_of_scroll):
        idx = int(num_of_scroll) - 1
        user_chosen_list = list_of_lists[idx]

        if is_try_not_empty_list(user_chosen_list):
            filter_way_num = input('Выберите номер способа фильтрации:\n(1) Получить только буквы\n\
(2) Получить только цифры\n(3) Получить знаки препинания и/или спецсимволы\n')

            if is_try_correct_filter_way_num(filter_way_num):
                sorted_list = sorting(user_chosen_list.copy(), filter_way_num)

                if is_try_not_empty_list(sorted_list):
                    user_chosen_list_and_sorted_list = [user_chosen_list, sorted_list]

    return user_chosen_list_and_sorted_list


def generate_list_of_lists() -> List[list]:

    list_of_lists = []

    for i in range(randint(1, 10)):
        list_of_lists.append([choice(printable) for _ in range(randint(0, 15))])
        num_in_scroll = i + 1
        print(f'({num_in_scroll}) {list_of_lists[i]}')

    return list_of_lists


def is_try_correct_entered_num_of_scroll(num_of_scroll: str, max_num_of_scroll: int) -> bool:

    flag = False

    try:
        if int(num_of_scroll) <= 0:
            raise NonPositiveScrollNumberError()

        elif int(num_of_scroll) > max_num_of_scroll:
            raise MaxScrollNumberError()

    except (NonPositiveScrollNumberError, MaxScrollNumberError):
        print('Выбранный номер списка за рамками предложенных вариантов.')
    except ValueError:
        print('Это не номер списка.')

    else:
        flag = True

    return flag


def is_try_not_empty_list(some_list: list) -> bool:

    flag = False

    try:
        if not some_list:
            raise EmptyListError()

    except EmptyListError:
        print('Список пуст.')

    else:
        flag = True

    return flag


def is_try_correct_filter_way_num(filter_way_num: str) -> bool:

    flag = False

    try:
        is_not_correct_filter_way_num = int(filter_way_num) != 1 and int(filter_way_num) != 2 and int(filter_way_num) != 3

        if is_not_correct_filter_way_num:
            raise FilterWayError()

    except FilterWayError:
        print('Такого варианта фильтрации нет.')
    except ValueError:
        print('Это не номер способа фильтрации.')

    else:
        flag = True

    return flag


def sorting(lst: List[str], filter_way_num: str) -> List[str]:

    new_lst = []

    for elem in lst:
        if create_condition_for_list_elem(elem, filter_way_num):
            new_lst.append(elem)

    return new_lst


def create_condition_for_list_elem(elem: str, cond_num: str) -> bool:

    conditions = {
        '1': elem.isalpha(),
        '2': elem.isdigit(),
        '3': not(elem.isalpha() or elem.isdigit())
    }

    return conditions[cond_num]


def string_encryption() -> list:

    string_encryption_out_list = []
    encryption_way_num = input('Выберите вариант действия для преобразования текста:\n(1) Зашифровать\n(2) Расшифровать\n')

    if is_try_correct_choice_encryption_way(encryption_way_num):
        user_string = input('Введите русские символы: ')

        if is_try_correct_input_string(user_string):
            user_key = input('Введите ключ: ')

            if is_try_correct_input_key(user_key):

                way_coefficient = {
                    1: 1,
                    2: -1
                }

                new_string = cesar_code(user_string, int(user_key) * way_coefficient[int(encryption_way_num)])

                string_encryption_out_list = [user_string, new_string, int(user_key), int(encryption_way_num)]

    return string_encryption_out_list


def is_try_correct_choice_encryption_way(encryption_way_num: str) -> bool:

    flag = False

    try:
        is_not_number_choice = int(encryption_way_num) != 1 and int(encryption_way_num) != 2

        if is_not_number_choice:
            raise EncryptionWayError()

    except EncryptionWayError:
        print('Выбранный номер действия со строкой за рамками предложенных вариантов.')
    except ValueError:
        print('Это не номер варианта действия.')

    else:
        flag = True

    return flag


def is_try_correct_input_string(string: str) -> bool:

    flag = False

    try:
        if not string:
            raise EmptyStringError()

        elif not is_all_ru_symbols(string):
            raise NonRussianSymbolError()

    except EmptyStringError:
        print('Не введена строка для шифрования.')
    except NonRussianSymbolError:
        print('Введена некорректная строка, присутствуют символы не из русского алфавита.')

    else:
        flag = True

    return flag


def is_try_correct_input_key(key: str) -> bool:

    flag = False

    try:
        if int(key) == 0:
            raise ZeroKeyEncryptionError()
        elif int(key) < 0:
            raise NegativeKeyEncryptionError()

    except ZeroKeyEncryptionError:
        print('Строка прежняя.')
    except (ValueError, NegativeKeyEncryptionError):
        print('Введен некорректный ключ.')

    else:
        flag = True

    return flag


def is_all_ru_symbols(string: str) -> bool:

    flag = True

    for symbol in string:

        is_not_symbol_ru = symbol not in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'

        if is_not_symbol_ru:
            flag = False
            break

    return flag


def cesar_code(string: str, key: int) -> str:

    new_string = ''

    for letter in string:

        is_capital_letter = 1040 <= ord(letter) <= 1071
        is_small_letter = 1072 <= ord(letter) <= 1103

        coefficient = {
            is_capital_letter: 1040,
            is_small_letter: 1072
        }

        ascii_shift_num = (((ord(letter) - coefficient[True]) + key) % 32) + coefficient[True]
        new_string += chr(ascii_shift_num)

    return new_string


def data_for_output(user_menu_choice: int) -> dict:

    data = {}

    if user_menu_choice == 1:  # Фильтрация листов

        list_filtering_out = list_filtering()

        if len(list_filtering_out) == 2:
            data = {
                'user_chosen_list': list_filtering_out[0],
                'sorted_list': list_filtering_out[1],
                'user_menu_choice': user_menu_choice
            }

    elif user_menu_choice == 2:  # Шифрование строки

        string_encryption_out = string_encryption()

        if len(string_encryption_out) == 4:
            data = {
                'user_string': string_encryption_out[0],
                'new_string': string_encryption_out[1],
                'key': string_encryption_out[2],
                'encryption_way_num': string_encryption_out[2],
                'user_menu_choice': user_menu_choice
            }

    return data


def is_try_correct_output_way_num(way: str) -> bool:

    flag = False

    try:
        if not (int(way) == 1 or int(way) == 2 or int(way) == 3 or int(way) == 4):
            raise OutputWayError()

    except OutputWayError:
        print('Выбранный номер способа вывода данных за рамками предложенных вариантов.')
    except ValueError:
        print('Это не номер способа вывода данных.')

    else:
        flag = True

    return flag


def output(data: dict, way: int):

    if int(way) == 1:
        printer(data)
    elif int(way) == 2:
        file_entry(data)
    elif int(way) == 3:
        database_entry()  # TODO "data" на входе функции
    elif int(way) == 4:
        post_request_sending()  # TODO "data" на входе функции


def printer(data: dict):

    is_list_filtering_works = data['user_menu_choice'] == 1
    is_string_encryption_works = data['user_menu_choice'] == 2

    if is_list_filtering_works:
        print('Выбранный список:', data['user_chosen_list'], '\nОтсортированный:', data['sorted_list'])

    elif is_string_encryption_works:

        word = {
            1: 'зашифрована',
            2: 'расшифрована'
        }

        print(f'Строка {data["user_string"]} {word[data["encryption_way_num"]]} '
              f'шифром Цезаря в строку {data["new_string"]} с ключом {data["key"]}.')


def file_entry(data: dict):

    is_list_filtering_works = data['user_menu_choice'] == 1
    is_string_encryption_works = data['user_menu_choice'] == 2

    if is_string_encryption_works:
        try_record_string_to_file(data['new_string'])

    elif is_list_filtering_works:
        try_record_lists_to_files(data['user_chosen_list'], data['sorted_list'])


def try_record_string_to_file(string: str):

    if string:
        try:
            with open('string.txt', 'w', encoding='utf-8') as output_file:
                print(string, end=' ', file=output_file)
        except:  # TODO OSError ?
            print('Ошибка при записи строки файл.')


def try_record_lists_to_files(user_chosen_list: list, sorted_list: list):

    if user_chosen_list and sorted_list:

        try:
            with open('user_chosen_list.bin', 'wb') as file_1, open('sorted_list.bin', 'wb') as file_2:
                pickle.dump(user_chosen_list, file_1)
                pickle.dump(sorted_list, file_2)
        except:  # TODO OSError ?
            print('Ошибка при записи выбранного и отсортированного списков в файлы.')


def database_entry():

    pass


def post_request_sending():

    pass
