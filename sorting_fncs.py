def insert_sort(a):
    n = len(a)

    for top in range(1, n):
        k = top
        while k > 0 and a[k - 1][1] > a[k][1]:
            a[k], a[k - 1] = a[k - 1], a[k]
            k -= 1


def choice_sort(a):
    n = len(a)

    for pos in range(0, n - 1):
        for k in range(pos + 1, n):
            if a[k][1] < a[pos][1]:
                a[k], a[pos] = a[pos], a[k]


def bubble_sort(a):
    n = len(a)

    for bypass in range(1, n):
        for k in range(0, n - bypass):
            if a[k][1] > a[k + 1][1]:
                a[k], a[k + 1] = a[k + 1], a[k]


def merge(a, b):
    c = [0] * (len(a) + len(b))
    i = k = n = 0

    while i < len(a) and k < len(b):
        if a[i][1] <= b[k][1]:
            c[n] = a[i]
            i += 1
            n += 1
        else:  # a[i][1] > b[k][1]
            c[n] = b[k]
            k += 1
            n += 1

    while i < len(a):
        c[n] = a[i]
        i += 1
        n += 1

    while k < len(b):
        c[n] = b[k]
        k += 1
        n += 1

    return c


def merge_sort(a):
    if len(a) <= 1:
        return

    middle = len(a) // 2
    left, right = a[:middle], a[middle:]

    merge_sort(left)
    merge_sort(right)

    c = merge(left, right)

    for i in range(len(a)):
        a[i] = c[i]


def toni_hoar_sort(a: list):
    if len(a) <= 1:
        return

    barrier = a[0][1]  # в идеале сделать случайным элементом из а
    left, middle, right = [], [], []

    for x in a:
        if x[1] < barrier:
            left.append(x)
        elif x[1] == barrier:
            middle.append(x)
        else:  # x[1] > barrier
            right.append(x)

    toni_hoar_sort(left)
    toni_hoar_sort(right)

    k = 0
    for x in left + middle + right:
        a[k] = x
        k += 1
