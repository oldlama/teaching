def up_print(string):

    if string:
        print(string.upper())


def letters_count_print(string):

    if string:
        clear_string = ''

        for c in string:
            if c not in clear_string:
                clear_string += c

        for c in clear_string:
            print(f'{c} - {string.count(c)}')


def symbol_change_print(string):

    if string:
        old_symbol = input('Введите символ, который хотите заменить: ')
        new_symbol = input('Введите символ, на который хотите заменить: ')
        print(string.replace(old_symbol, new_symbol))


def words_from_string_print(string):

    if string:
        box = ''

        for c in string:
            if c.isalpha():
                box += c
            else:
                box += ' '

        box = box.split()

        for word in box:
            print(word)
