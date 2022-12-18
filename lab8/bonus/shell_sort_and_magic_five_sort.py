## skonczone
import random
from typing import List
import time
import math


def median_3(a, b, c):
    return max(min(a, b), min(c, max(a, b)))


def median_5(a, b, c, d, e):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    return median_3(e, f, g)

def median_less_than_5(lst: List):
    if len(lst) == 4:
        return min(max(lst[0], lst[1]), max(lst[2], lst[3]))
    elif len(lst) == 3:
        return median_3(lst[0], lst[1], lst[2])
    elif len(lst) == 2 or len(lst) == 1:
        return lst[0]


def divide_lst_to_5(lst):
    lst_of_lsts = []
    i = 0
    while True:
        if (i + 1) * 5 == len(lst):
            break
        elif (i + 1) * 5 > len(lst):
            lst_of_lsts.append(lst[5 * i:])
            break
        else:
            lst_of_lsts.append(lst[5 * i:5 * (i + 1)])
        i += 1
    return lst_of_lsts

def get_medians(lst_of_lsts):
    median_lst = []
    for lst in lst_of_lsts:
        if len(lst) == 5:
            median_lst.append(median_5(lst[0], lst[1], lst[2], lst[3], lst[4]))
        else:
            median_lst.append(median_less_than_5(lst))


    return  median_lst

def get_good_pivot(lst):
    divided = divide_lst_to_5(lst)
    median_lst = get_medians(divided)
    while len(median_lst) > 1:
        divided = divide_lst_to_5(median_lst)
        median_lst = get_medians(divided)
    if len(median_lst) == 1:
        return median_lst[0]
    else:
        return None


def is_sorted(lst):
    lst2 = lst[:]
    lst2.sort()
    if lst == lst2:
        print('sorted')
        return True
    else:
        print('unsorted')
        return False


def shell_sort(lst: List[int], how=None):
    lst_size = len(lst)
    if how is not None:
        if how == "half":
            start_step = len(lst) // 2
            divider = 2
    else:
        k = math.floor(math.log(lst_size / 3 * 2 + 1))
        if (3 ** k - 1) // 2 > lst_size / 3:
            k -= 1
        start_step = (3 ** k - 1) // 2
        divider = 3
    step = start_step
    while step > 0:

        for i in range(step, lst_size):
            index = i
            el = lst[i]
            while index >= step and lst[index - step] > el:
                lst[index] = lst[index - step]
                index -= step

            lst[index] = el

        step //= divider


def quicksort(lst, median=False):
    if len(lst) < 1:
        return lst
    if median is False:
        pivot = lst[0]
    else:
        pivot = get_good_pivot(lst)
    i = 0
    j = len(lst) - 1
    smaller = []
    bigger = []
    equal = []
    for i in range(len(lst)):
        if lst[i] < pivot:
            smaller.append(lst[i])
        elif lst[i] > pivot:
            bigger.append(lst[i])
        else:
            equal.append(lst[i])

    return quicksort(smaller) + equal + quicksort(bigger)


lst2 = []
for i in range(10000):
    lst2.append(random.randint(0, 100))

lst_3 = lst2[:]
lst_2 = lst2[:]
lst_q_m = lst2[:]
lst_q = lst2[:]
lst_sorted = lst2[:]
lst_sorted.sort()

print("shell, wersja dla (3k-1)/2:")
t_start = time.perf_counter()
shell_sort(lst_3)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format((t_stop - t_start) * 1000) + " ms")

print("shell, wersja dla podziału na połowe:")
t_start = time.perf_counter()
shell_sort(lst_2, "half")
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format((t_stop - t_start) * 1000) + " ms")
## dla tego rozmiaru działa szybciej od heapsorta, lecz należy zauważyć, że implementacja heapsorta była z wykonaniem obiektow HeapEl, które powodowały zwiększanie
## potrzebnej pamięci do przekopiowania


lst2 = []
for i in range(10000):
    lst2.append(random.randint(0, 100))
lst_q_m = lst2[:]
lst_q = lst2[:]
lst_sorted = lst2[:]
lst_sorted.sort()
print("quicksort, wersja dla magicznych piątek:")
t_start = time.perf_counter()
lst_q = quicksort(lst_q, median=True)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format((t_stop - t_start) * 1000) + " ms")

print("quicksort, wersja dla pierwszego elementu:")
t_start = time.perf_counter()
lst_q_m = quicksort(lst_q_m, median=False)
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format((t_stop - t_start) * 1000) + " ms")
print("is equal:", lst_q == lst_q_m)

## algorytmy mają podobny czas wykonywania, dala zbioru 10000 elementów, nie widać przewagi algorytmu magicznych piątek, a nawet jest trochę wolniejsze z uwagi na konieczność
## obliczania mediany median. Różnica powinna być widoczna dla znacznie większych zbiorów danych, ponieważ dla zwykłego quicksorta O(n log n),
## a magicznych piątek O(n), ponadto wybieranie pierwszego elementu może spowodować zbyt głęboką rekurencje i O(n^2), co da się rozwiązać wybierając losowy element