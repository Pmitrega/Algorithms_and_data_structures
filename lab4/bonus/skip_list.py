#skończone
#lista nie wyświetla się poprawnie w tym terminalu, bo zwija ją do następnej linii
from typing import List, Union
from random import random


class SkipListEl:
    def __init__(self, key: Union[int, None], data, height):
        self.key = key
        self.height = height
        self.data = data
        self.nexts = [None for i in range(height)]

    def __str__(self):
        st = "[\n"
        for i in range(self.height):
            st += "next \n"
        st += str(self.key) + " \n"
        st += str(self.data) + " \n"
        st += "]"
        return st


class SkipList:
    def __init__(self, max_level: int):
        self.max_level = max_level
        self.head = SkipListEl(None, None, max_level)

    def search(self, key: int):
        curr_el = self.head
        found = False
        layer = self.max_level - 1
        while layer >= 0:
            if curr_el.nexts[layer] is None:
                if layer == 0:
                    print("not found")
                    return
                else:
                    layer -= 1
                    continue
            elif curr_el.nexts[layer].key == key:
                return curr_el.nexts[layer].data
            elif key < curr_el.nexts[layer].key:
                layer -= 1
                continue
            elif key > curr_el.nexts[layer].key:
                curr_el = curr_el.nexts[layer]
        print("not found")
        return None

    def insert(self, key: int, data, height=None):
        path = [None for i in range(self.max_level)]
        layer = self.max_level - 1
        if height is None:
            height = self.randomLevel()
        new_node = SkipListEl(key, data, height)
        curr_el = self.head
        while layer >= 0:
            if curr_el.nexts[layer] is None:
                if layer == 0:
                    path[layer] = curr_el
                    break
                else:
                    path[layer] = curr_el
                    layer -= 1
                    continue
            elif curr_el.nexts[layer].key == key:
                curr_el.nexts[layer].data = data
                return None
            elif key < curr_el.nexts[layer].key:
                path[layer] = curr_el
                layer -= 1
                continue
            elif key > curr_el.nexts[layer].key:
                curr_el = curr_el.nexts[layer]

        for i in range(len(path)):
            if i < new_node.height:
                n = path[i].nexts[i]
                path[i].nexts[i] = new_node
                new_node.nexts[i] = n
        return 0

    def remove(self, key: int):
        path = [None for i in range(self.max_level)]
        layer = self.max_level - 1
        curr_el = self.head
        to_remove = None
        while layer >= 0:
            if curr_el.nexts[layer] is None:
                if layer == 0:
                    path[layer] = curr_el
                    break
                else:
                    path[layer] = curr_el
                    layer -= 1
                    continue
            elif curr_el.nexts[layer].key == key:
                path[layer] = curr_el
                if to_remove is None:
                    to_remove = curr_el.nexts[layer]
                layer -= 1
                continue
            elif key < curr_el.nexts[layer].key:
                path[layer] = curr_el
                layer -= 1
                continue
            elif key > curr_el.nexts[layer].key:
                curr_el = curr_el.nexts[layer]
        if to_remove is not None:
            for i in range(to_remove.height):
                path[i].nexts[i] = to_remove.nexts[i]
        else:
            raise IndexError("key not found")

    def randomLevel(self):
        lvl = 1
        while random() < 0.5 and lvl < self.max_level:
            lvl = lvl + 1
        return lvl

    def __str__(self):
        curr = self.head
        lay = ["" for i in range(self.max_level)]
        data = ""
        keys = ""
        st = ""
        default = " " * 10
        while curr is not None:
            for i in range(self.max_level):
                if len(curr.nexts) > i:
                    lay[i] += "next" + default[:-len("next")]
                else:
                    lay[i] += default
            data += str(curr.data) + default[:-len(str(curr.data))]
            keys += str(curr.key) + default[:-len(str(curr.key))]
            curr = curr.nexts[0]

        for i in range(self.max_level):
            st += lay[self.max_level - 1 - i] + '\n'
        st += data + "\n"
        st += keys + "\n"
        return st


skip_lst = SkipList(4)
for i in range(1, 16):
    skip_lst.insert(i, chr(ord('a') + i - 1))
print(skip_lst)
print(skip_lst.search(2))
skip_lst.insert(2, "Z")
print(skip_lst.search(2))
skip_lst.remove(5)
skip_lst.remove(6)
skip_lst.remove(7)
print(skip_lst)
skip_lst.insert(6, "W")
print(skip_lst)
print("Odwrotnie ----------")
for i in range(1, 16):
    skip_lst.insert(16 - i, chr(ord('a') + i - 1))
print(skip_lst)
print(skip_lst.search(2))
skip_lst.insert(2, "Z")
print(skip_lst.search(2))
skip_lst.remove(5)
skip_lst.remove(6)
skip_lst.remove(7)
print(skip_lst)
skip_lst.insert(6, "W")
print(skip_lst)
