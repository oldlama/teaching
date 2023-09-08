def fnc_2(f2_arg_1, f2_arg_2):
    print(f'fnc_2(f2_arg_1, f2_arg_2), f2_arg_1 = {f2_arg_1}, f2_arg_2 = {f2_arg_2}')


def fnc_1(f1_arg_1, f1_arg_2):
    print(f'fnc_1(f1_arg_1, f1_arg_2), f1_arg_1 = {f1_arg_1}, f1_arg_2 = {f1_arg_2}')
    fnc_2(f2_arg_1, f2_arg_2)


f2_arg_1 = 3
f2_arg_2 = 4
fnc_1(1, 2)
