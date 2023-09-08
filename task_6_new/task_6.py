from task_6_funcs import *


if __name__ == '__main__':

    user_choice = input('Выберите номер пункта:\n(1) Фильтрация листов\n(2) Шифрование строки\n')

    if is_try_menu_variants(user_choice):
        data = data_for_output(int(user_choice))

        if data:
            way = input('Введите номер способа вывода данных:\n(1) Вывод в панель "Run"\n\
(2) Вывод в файл(ы)\n(3) Вывод в базу данных\n(4) Отправка post-запросом\n')

            if is_try_correct_output_way_num(way):
                output(data, int(way))
