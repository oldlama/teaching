from task_6_funcs import *


if __name__ == '__main__':

    try:
        user_choice = int(input('Выберите номер пункта:\n(1) Фильтрация листов\n(2) Шифрование строки\n'))
        if not (user_choice == 1 or user_choice == 2):
            raise StartWayError('Несуществующий номер для выбора варианта работы программы.')

        elif user_choice == 1:
            try:

                output(lists_filtering())

            except (NonPositiveListNumberError, IndexError):
                print('Выбранный номер списка за рамками предложенных вариантов.')
            except FilterWayError:
                print('Такого варианта фильтрации нет.')
            except EmptyListError:
                print('Список пуст.')

        else:  # elif user_choice == 2:

            output(string_encryption())

    except StartWayError:  # файл исключений подтягивается из-за импорта функций, где он уже импортирован?
        print('Выбранный номер действия для начала программы за рамками предложенных вариантов.')
    except EncryptionWayError:
        print('Выбранный номер действия со строкой за рамками предложенных вариантов.')
    except NonRussianSymbol:
        print('Введена некорректная строка.')
    except ZeroKeyEncryption:
        print('Строка прежняя.')
    except EmptyStringError:
        print('Строка пуста.')
    except ValueError:
        print('Это не номер.')
    # except DataTypeError:
    #     print('Некорректный тип данных для вывода.')
    # except FileDataTypeError:
    #     print('Некорректный тип данных для записи в файл.')
