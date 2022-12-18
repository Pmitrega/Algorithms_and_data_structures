#skonczone
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
    def __init__(self):
        self.size = 0
        self.tab = []
        pass

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def peek(self):
        if not self.is_empty():
            return self.tab[0]
        else:
            return None

    def dequeue(self):
        if self.is_empty():
            return None
        el = self.tab[0]
        self.tab[0] = self.tab[self.size - 1]
        i = 0
        lci = self.left(i)
        rci = self.right(i)
        while lci < self.size and rci < self.size:
            if self.tab[i] < self.tab[lci] or self.tab[i] < self.tab[rci]:
                if self.tab[rci] <= self.tab[lci]:
                    self.tab[i], self.tab[lci] = self.tab[lci], self.tab[i]
                    i = lci
                else:
                    self.tab[i], self.tab[rci] = self.tab[rci], self.tab[i]
                    i = rci
                lci = self.left(i)
                rci = self.right(i)
            else:
                break
        self.tab = self.tab[:-1]
        self.size -=1
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
        if self.is_empty():
            print('{ }')
            return
        print ('{', end=' ')
        for i in range(self.size-1):
            print(self.tab[i], end = ', ')
        if self.tab[self.size-1]: print(self.tab[self.size-1] , end = ' ')
        print( '}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)


heap = Heap()
arr = [4, 7, 6, 7, 5, 2, 2, 1]
st = "ALGORYTM"
for i in range(len(arr)):
    heap.enqueue(HeapEl(arr[i], st[i]))
heap.print_tree(0, 0)
heap.print_tab()
print(heap.dequeue())
print(heap.peek())
heap.print_tab()

while not heap.is_empty():
    print(heap.dequeue())
heap.print_tab()