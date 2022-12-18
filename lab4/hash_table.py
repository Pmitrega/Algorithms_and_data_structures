#skonczone
from typing import Union


class HashArrayElement:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class HashArray:
    def __init__(self, size: int, c1: int = 1, c2: int = 0):
        self.size = size
        self.c1 = c1
        self.c2 = c2
        self.tab = [None for i in range(size)]

    def __hash(self, key: Union[int, str], i):
        if isinstance(key, str):
            t_k = 0
            for l in key:
                t_k += ord(l)
            key = t_k
        return (key % self.size + i * self.c1 + i ** 2 * self.c2) % self.size

    def insert(self, key: Union[str, int], data):
        i = 0
        while self.tab[self.__hash(key, i)] is not None:
            if self.tab[self.__hash(key, i)].key == key:
                # print("zamiana danej")
                self.tab[self.__hash(key, i)].data = data
                return
            if self.tab[self.__hash(key, i)].data is None:
                break
            if i == self.size:
                print("Brak miejsca")
                return
            i += 1
        self.tab[self.__hash(key, i)] = HashArrayElement(key, data)

    def search(self, key) -> Union[None, HashArrayElement]:
        i = 0
        while self.tab[self.__hash(key, i)] is not None:
            if self.tab[self.__hash(key, i)].key == key:
                return self.tab[self.__hash(key, i)]
            if i == self.size:
                print("Brak danej")
                return None
            i += 1

        print("Brak danej")
        return None

    def __str__(self):
        st = "{"
        inside = False
        for i in self.tab:
            if i is not None:
                st += str(i.key) + ":" + str(i.data) + ","
                inside = True
        if inside:
            st = st[:-1]
        st += "}"

        return st

    def remove(self, key):
        i = 0
        while self.tab[self.__hash(key, i)] is not None:
            if self.tab[self.__hash(key, i)].key == key:
                self.tab[self.__hash(key, i)].data = None
                return
            if self.tab[self.__hash(key, i + 1)] == self.tab[self.__hash(key, 0)]:
                print("Brak danej")
            i += 1

        print("Brak danej")
        return


def test1(size, c1=1, c2=0):
    ha = HashArray(size, c1, c2)
    for i in range(1, 16):
        key = i
        if i == 6:
            key = 18
        if i == 7:
            key = 31
        ha.insert(key, chr(ord('A') + i - 1))
    print(ha)

    s1 = ha.search(5)
    print(s1.data)
    s2 = ha.search(14)
    print(s2)

    ha.insert(5, "Z")
    print(ha.search(5).data)
    ha.remove(5)
    print(ha)
    print(ha.search(31).data)
    ha.insert("test", "W")
    print(ha)


def test2(size=13, c1=1, c2=0):
    ha = HashArray(size, c1, c2)
    for i in range(1, 16):
        key = i * 13
        ha.insert(key, chr(ord('A') + i - 1))
    print(ha)


print("---test2-1---")
test2(13, 1, 0)
print("---test2-2---")
test2(13, 0, 1)
print("---test1---")
test1(13, 0, 1)