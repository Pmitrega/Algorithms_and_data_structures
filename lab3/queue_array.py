#skończone
from typing import List


def realloc(tab, size):
    old_size = len(tab)
    return [tab[i] if i < old_size else None for i in range(size)]


class Queue:
    tab: List
    length: int
    read_ind: int
    write_ind: int

    def __init__(self):
        self.tab = [None for i in range(5)];
        self.length = 5
        self.write_ind = 0
        self.read_ind = 0

    def is_empty(self):
        return self.read_ind == self.write_ind

    def peek(self):
        return self.tab[self.read_ind]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            data = self.tab[self.read_ind]
            self.tab[self.read_ind] = None
            self.read_ind = (self.read_ind + 1) % self.length
            return data

    def enqueue(self, el):
        self.tab[self.write_ind] = el
        self.write_ind = (self.write_ind + 1) % self.length
        if self.write_ind == self.read_ind:
            self.tab = realloc(self.tab, self.length * 2)
            for i in range(self.length - self.read_ind):
                self.tab[self.read_ind + self.length + i] = self.tab[self.read_ind + i]
                self.tab[self.read_ind + i] = None
            self.read_ind = self.read_ind + self.length
            self.length = 2 * self.length

    def tab_str(self):
        return str(self.tab)

    def __str__(self):
        if self.is_empty():
            return "[]"
        r_str = "["
        i = self.read_ind
        while i != self.write_ind:
            r_str += str(self.tab[i]) + ', '
            i = (i+1)%self.length

        r_str = r_str[:-2]
        r_str += ']'
        return r_str

queue = Queue()

for i in range(1,5):
    queue.enqueue(i)
print(queue.dequeue())
print(queue.peek())
print(queue)
for i in range(5, 9):
    queue.enqueue(i)
print(queue.tab_str())

while not queue.is_empty():
    print(queue.dequeue())

print(queue)
