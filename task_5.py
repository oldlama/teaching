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
# nums_upward = sorted(set(nums_from_0_to_20))
# nums_downward = sorted(set(nums_from_0_to_20), reverse=True)
# box_1, box_2 = [], []
#
# for num in tuple(set(nums_from_0_to_20)):
#     box_1.append(num) if num % 3 == 0 else box_2.append(num)  # как можно меньше строк :D
#
# print(*nums_upward)
# print(*nums_downward)
# print(*(box_1 + box_2))

#5
# from random import randint, choice
#
# statuses = ('backlog', 'in_work', 'done')
# l_of_ls = [list((randint(0, 1000), choice(statuses))) for _ in range(1000)]
#
# box = list(filter(lambda x: x[1] == 'backlog', l_of_ls))
# box += list(filter(lambda x: x[1] == 'in_work', l_of_ls))
# box += list(filter(lambda x: x[1] == 'done', l_of_ls))
#
# print(box)
