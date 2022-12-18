##skonczone
import random
import time


class HeapEl:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __eq__(self, other):
        return other.key == self.key

    def __gt__(self, other):
        return self.key > other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __str__(self):
        return str(self.key) + " : " + str(self.val)


class Heap:
    def __init__(self, lst=None):
        if lst is None:
            self.size = 0
            self.tab = []
        else:
            self.tab = lst
            self.size = len(lst)
            self.heapify()

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def peek(self):
        if len(self.tab) > 0:
            return self.tab[0]
        else:
            return None

    def move_down(self, index):
        i = index
        lci = self.left(i)
        rci = self.right(i)
        while lci < self.size:
            if rci >= self.size:
                if self.tab[i] < self.tab[lci]:
                    self.tab[i], self.tab[lci] = self.tab[lci], self.tab[i]
                    i = lci
                else:
                    break
            elif self.tab[lci] > self.tab[rci]:
                if self.tab[i] < self.tab[lci]:
                    self.tab[i], self.tab[lci] = self.tab[lci], self.tab[i]
                    i = lci
                else:
                    break
            elif self.tab[lci] == self.tab[rci]:
                if self.tab[i] < self.tab[lci]:
                    self.tab[i], self.tab[lci] = self.tab[lci], self.tab[i]
                    i = lci
                else:
                    break
            elif self.tab[lci] < self.tab[rci]:
                if self.tab[i] < self.tab[rci]:
                    self.tab[i], self.tab[rci] = self.tab[rci], self.tab[i]
                    i = rci
                else:
                    break

            lci = self.left(i)
            rci = self.right(i)

    def heapify(self):
        i = self.parent(self.size)
        while i >= 0:
            self.move_down(i)
            i -= 1
        self.move_down(0)

    def dequeue(self):
        el = self.tab[0]
        self.tab[0] = self.tab[self.size - 1]
        self.tab[self.size - 1] = el
        self.size -= 1
        i = 0
        self.move_down(i)
        return el

    def enqueue(self, val):
        self.tab.append(val)
        i = len(self.tab) - 1
        while i > 0 and self.tab[self.parent(i)] < self.tab[i]:
            self.tab[self.parent(i)], self.tab[i] = self.tab[i], self.tab[self.parent(i)]
            i = self.parent(i)
        self.size += 1

    def left(self, idx):
        # żeby indeksowanie było od 1 dodaje 1
        i = idx + 1
        # potem tylko odejmuje
        return 2 * i - 1

    def right(self, idx):
        i = idx + 1
        return 2 * i

    def parent(self, idx):
        idx += 1
        if idx > 1:
            return idx // 2 - 1
        else:
            raise IndexError("First element don't have parent")

    def print_tab(self):
        print('{', end=' ')
        for i in range(self.size - 1):
            print(self.tab[i], end=', ')
        if not self.is_empty() and self.tab[self.size - 1]: print(self.tab[self.size - 1], end=' ')
        print('}')

    def print_tab2(self):
        for i in range(len(self.tab)):
            print(self.tab[i])

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

    def heapsort(self):
        while self.size > 0:
            self.dequeue()
        return self.tab


def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i].key > lst[i + 1].key:
            return False
    return True


def selectionSort_swap(lst):
    for i in range(len(lst)):
        minimum = lst[i].key
        min_index = i
        for j in range(i, len(lst)):
            if lst[j].key < minimum:
                minimum = lst[j].key
                min_index = j
        if i != min_index:
            lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst


def selectionSort_shift(lst):
    i = 0
    size = len(lst)
    while size > 0:
        j = 1
        min_index = 0
        minimum = lst[0]
        while j < size:
            if lst[j] < minimum:
                minimum = lst[j]
                min_index = j
            j += 1

        lst.append(minimum)
        lst.pop(min_index)
        size -=1
    return lst


lst = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
for el in lst:
    el = HeapEl(el[0], el[1])
h = Heap(lst)
h.heapsort()
h.print_tab2()
lst2 = []
for i in range(10000):
    r = random.randint(0, 1000)
    lst2.append(HeapEl(r, r))
lst_h = lst2[:]
lst_s_1000 = lst2[:]
lst_shift_1000 = lst2[:]
h2 = Heap(lst_h)
t_start = time.perf_counter()
h2.heapsort()
t_stop = time.perf_counter()
print("Czas obliczeń (heap sort):", "{:.3f} ms".format((t_stop - t_start) * 1000))
if not is_sorted(h2.tab):
    print("not sorted")




print("\n -------------- selection sort -----------------")
lst = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
for i in range(len(lst)):
    lst[i] = HeapEl(lst[i][0], lst[i][1])
lst_swap = lst[:]
lst_shift = lst[:]

selectionSort_swap(lst_swap)
print("\n swap -----------------")
for el in lst_swap:
    print("(",el.key, ",", el.val, ")")

selectionSort_shift(lst_shift)
print("\n shift -----------------")
for el in lst_shift:
    print("(",el.key, ",", el.val, ")")


t_start = time.perf_counter()
selectionSort_swap(lst_s_1000)
t_stop = time.perf_counter()
print("Czas obliczeń selection sort (swap):", "{:.3f} ms".format((t_stop - t_start) * 1000))
if not is_sorted(lst_s_1000):
    print("not sorted")

t_start = time.perf_counter()
selectionSort_shift(lst_shift_1000)
t_stop = time.perf_counter()
print("Czas obliczeń selection sort (shift):", "{:.3f} ms".format((t_stop - t_start) * 1000))
if not is_sorted(lst_shift_1000):
    print("not sorted")


###przykładowe czasy obliczeń:
## 10000 el:
# heap_sort: 97 ms
# selection_sort_swap: 2430 ms
# selection_sort_shift: 6067 ms
## 20000 el:
# heap_sort: 212 ms
# selection_sort_swap: 9771 ms
# selection_sort_shift: 23795 ms

##widać wzorst nlogn dla heap sorta, a dla selection sorta n^2 co jest zgodne z teorią.
## ponadto selection_sort przez shifta jest mniej wydajny (przesuwanie elementów tablicy, więcej przypisań od zamiany dwóch elementów)
## przy czym algorytm poprzez shift jest stabilny.