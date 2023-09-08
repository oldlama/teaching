from random import randint, choice
from string import printable
from typing import List
from task_6_exceptions import *


def sorting(lst: List[str], filter_way_num: str) -> List[str]:

    if filter_way_num != '1' and filter_way_num != '2' and filter_way_num != '3':
        raise FilterWayError('Несуществующий номер для выбора фильтрации.')

    if filter_way_num == '1':
        for i in range(len(lst) - 1, -1, -1):
            if i < len(lst) and not 97 <= ord(lst[i].lower()) <= 122:
                del lst[i]
    elif filter_way_num == '2':
        for i in range(len(lst) - 1, -1, -1):
            if i < len(lst) and not 48 <= ord(lst[i]) <= 57:
                del lst[i]
    elif filter_way_num == '3':
        for i in range(len(lst) - 1, -1, -1):
            if i < len(lst) and (97 <= ord(lst[i].lower()) <= 122 or 48 <= ord(lst[i]) <= 57):
                del lst[i]

    return lst


def lists_filtering() -> list:

    box = []
    list_of_lists = []

    for i in range(randint(1, 10)):
        list_of_lists.append([choice(printable) for _ in range(randint(0, 15))])
        print(f'({i + 1}) {list_of_lists[i]}')

    num = int(input('Ведите номер списка: '))
    if num < 1:
        raise NonPositiveListNumberError('Введен неположительный номер для выбора списка.')

    user_list = list_of_lists[num - 1]
    if not user_list:
        raise EmptyListError('Список, выбранный для фильтрации, пустой.')
    else:

        filter_way_num = input('Выберите номер способа фильтрации:\n(1) Получить только буквы\n\
(2) Получить только цифры\n(3) Получить знаки препинания и/или спецсимволы\n')
        sorted_list = sorting(user_list.copy(), filter_way_num)

        if user_list and sorted_list:
            box = [user_list, sorted_list]
        elif not sorted_list:  # else:
            raise EmptyListError('Список после фильтрации пустой.')

    return box


def is_all_ru_symbols(string: str) -> bool:

    flag = True

    if string:
        for s in string:
            if not (1040 <= ord(s) <= 1071 or 1072 <= ord(s) <= 1103):
                flag = False
                break
    else:
        raise EmptyStringError('Нет строки для шифрования, она пустая.')

    return flag


def cesar_code(string: str, key: int) -> str:

    box = ''

    if key != 0:

        new_string = ''

        for letter in string:

            if 1040 <= ord(letter) <= 1071:
                ascii_shift_num = (((ord(letter) - 1040) + key) % 32) + 1040
                new_string += chr(ascii_shift_num)
            elif 1072 <= ord(letter) <= 1103:  # else:
                ascii_shift_num = (((ord(letter) - 1072) + key) % 32) + 1072
                new_string += chr(ascii_shift_num)
        if key > 0:
            box += f'Строка {string} зашифрована шифром Цезаря в строку {new_string} с ключом {key}.'
        else:
            box += f'Строка {string} расшифрована шифром Цезаря в строку {new_string} с ключом {key * (-1)}.'
    else:
        raise ZeroKeyEncryption('Нулевой ключ для шифрования, останется исходная строка. ')

    return box


def string_encryption() -> str:

    box = ''
    user_choice = int(input('(1) Зашифровать\n(2) Расшифровать\n'))  # int, т.к. игнорирует пробелы

    if user_choice != 1 and user_choice != 2:
        raise EncryptionWayError('Несуществующий номер для выбора действия со строкой.')
    else:
        user_string = input('Введите русские символы: ')

        if is_all_ru_symbols(user_string):
            user_key = int(input('Введите ключ: '))

            if user_choice == 1 and cesar_code(user_string, user_key):
                box += cesar_code(user_string, user_key)
            elif user_choice == 2 and cesar_code(user_string, user_key):
                box += cesar_code(user_string, user_key * (-1))

        else:
            raise NonRussianSymbol('Были введены символы не из русского алфавита.')

    return box


def printer(data):

    if type(data) == str:
        print(data)
    elif type(data) == list:
        print(*data, sep='\n')
    # else:
    #    raise DataTypeError('Тип данных для вывода не является списковым или строковым.')


def file_entry(data):

    if type(data) == list:  # если сработала фильтрация списка
        with open('out.txt', 'w', encoding='utf-8') as output_file:
            for el_1 in data[0]:
                print(el_1, end=' ', file=output_file)
            print(file=output_file)
            for el_2 in data[-1]:
                print(el_2, end=' ', file=output_file)
    elif type(data) == str:  # если сработала шифровка
        with open('out.txt', 'w', encoding='utf-8') as output_file:
            print(data, end=' ', file=output_file)
    # else:
    #    raise FileDataTypeError('Возникла ошибка работы с записью данных в файл.')


def database_entry(data):

    pass


def post_request_sending(data):

    pass


def output(data, way='printer'):

    if way == 'printer':
        printer(data)
    elif way == 'вывод в файл':
        file_entry(data)
    elif way == 'вывод в базу данных':
        database_entry(data)
    elif way == 'отправка post-запросом':
        post_request_sending(data)
