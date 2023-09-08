def up_print(string): #Правильно

    if string:
        print(string.upper())


def letters_count_print(string): #Правильно

    if string:
        clear_string = ''

        for c in string:
            if c not in clear_string:
                clear_string += c  #Для подобного всё же лучше использовать лист, а не строку

        for c in clear_string:
            print(f'{c} - {string.count(c)}')


def symbol_change_print(string): #Всё нормально

    if string:
        old_symbol = input('Введите символ, который хотите заменить: ')
        new_symbol = input('Введите символ, на который хотите заменить: ')
        print(string.replace(old_symbol, new_symbol))


def words_from_string_print(string): #Неправильно

    if string:
        box = ''

        for c in string:
            if c.isalpha():  ##Данный метод уберет так же цирфы, и остальные знаки. Это неправильно. НАпример при вводе
                #емейла бот отработает совсем некорректно
                box += c
            else:
                box += ' '

        box = box.split()

        for word in box:
            print(word)
