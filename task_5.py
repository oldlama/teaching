# 1
# интересны примеры zip(), где он лучше всего подходит на практике

# 2
# list - изменяемый, tupple - неизменяемый, зато работает быстрее

#3
# soldiers = ('Oleg', 'Ivan', 'Katya')
#
# for i, j in enumerate(soldiers):
#     print(f'{i+1} - {j}')

# 4
# from random import randint
#
# nums_from_0_to_20 = [randint(0, 20) for _ in range(1000)]
#
# print(set(sorted(nums_from_0_to_20)))
# print(set(sorted(nums_from_0_to_20, reverse=True)))
# print(sorted(set(nums_from_0_to_20), key=lambda x: x % 3))

#5
from random import randint, choice


def sort_condition(x):
    return x[1] == 'done', x[1] == 'in_work', x[1] == 'backlog'


statuses = ('backlog', 'in_work', 'done')
l_of_ls = [list((randint(0, 1000), choice(statuses))) for _ in range(1000)]

print(sorted(l_of_ls, key=sort_condition))

# print(list(filter(lambda x: x[1] == 'backlog', l_of_ls)), end=' ')
# print(list(filter(lambda x: x[1] == 'in_work', l_of_ls)), end=' ')
# print(list(filter(lambda x: x[1] == 'done', l_of_ls)), end=' ')
