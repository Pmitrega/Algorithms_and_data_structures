##skonczone
import copy
from typing import List

BASE_SIZE = 6


class EnrolledListEl:
    tab: List

    def __init__(self):
        self.tab = [None for i in range(BASE_SIZE)]
        self.next = None
        self.num_of_el = 0

    def get(self, index):
        n = self
        while n is not None and index >= n.num_of_el:
            index -= n.num_of_el
            if n.next is None:
                raise ValueError("out of range")
            n = n.next

        return n.tab[index]

    def __str__(self):
        n = self
        st = "[\n"
        while n is not None:
            st += str(n.tab) + "[" + str(n.num_of_el) + "]" '\n'
            n = n.next

        st += ']'
        return st

    def __move_half(self, n):
        tem = n.next
        n.next = EnrolledListEl()
        n.next.next = tem
        n.next.num_of_el = BASE_SIZE // 2
        n.num_of_el = BASE_SIZE // 2

        for i in range(BASE_SIZE // 2):
            n.next.tab[i] = n.tab[BASE_SIZE // 2 + i]
            n.tab[BASE_SIZE // 2 + i] = None

    def __move_right(self, index, n):
        if index == BASE_SIZE - 1:
            return
        i = index
        while n.tab[i] is not None:
            i += 1
        while i >= index:
            if i + 1 == BASE_SIZE:
                i -= 1
                continue
            n.tab[i + 1], n.tab[i] = n.tab[i], n.tab[i + 1]
            i -= 1


    def __move_left(self, index, n):
        i = index
        while n.tab[i] is None:
            if i + 1 == BASE_SIZE:
                break
            n.tab[i + 1], n.tab[i] = n.tab[i], n.tab[i + 1]
            i += 1

    def insert(self, el, index):
        n = self
        while n is not None:
            if n.num_of_el == BASE_SIZE and (index - n.num_of_el) <= 0:
                self.__move_half(n)
            elif n.num_of_el < BASE_SIZE and (index - n.num_of_el <= 0):
                self.__move_right(index, n)
                n.tab[index] = copy.deepcopy(el)
                n.num_of_el += 1
                break
            elif n.num_of_el == BASE_SIZE and (index - n.num_of_el > 0) and n.next is None:
                n.next = EnrolledListEl()
                n.next.num_of_el = 1
                n.next.tab[0] = copy.deepcopy(el)
                break
            elif n.num_of_el < BASE_SIZE and (index - n.num_of_el > 0) and n.next is None:
                n.tab[n.num_of_el] = copy.deepcopy(el)
                n.num_of_el += 1
                break
            elif index - n.num_of_el == 0:
                n.tab[index] = copy.deepcopy(el)
                n.num_of_el += 1
                break
            else:
                index -= n.num_of_el
                n = n.next

    def delete(self, index):
        n = self
        while n is not None and index >= n.num_of_el:
            index -= n.num_of_el
            if n.next is None:
                raise ValueError("out of range")
            n = n.next
        if n.next is None or n.num_of_el >= BASE_SIZE//2 + 1:
            n.tab[index] = None
            self.__move_left(index, n)
            n.num_of_el -= 1
            return
        if n.num_of_el < BASE_SIZE//2 +1:
            n.tab[index] = en_lst.next.tab[0]
            en_lst.next.tab[0] = None
            en_lst.next.num_of_el -= 1
            self.__move_left(0, en_lst.next)
            if n.next.num_of_el < BASE_SIZE//2:
                for i in range(n.next.num_of_el):
                    n.tab[i + n.num_of_el] = n.next.tab[i]
                n.num_of_el += n.next.num_of_el
                t = n.next.next
                n.next = t
            return


en_lst = EnrolledListEl()
for i in range(9):
    en_lst.insert(i + 1, i)
print(en_lst.get(4))
en_lst.insert(10, 1)
en_lst.insert(11, 8)
print(en_lst)
##jeśli chodziło o indeksy pierwotnej listy to (po usunieciu indexy się przesuwają):
# en_lst.delete(1)
# en_lst.delete(1)
en_lst.delete(1)
en_lst.delete(2)
print(en_lst)