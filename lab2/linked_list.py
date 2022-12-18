#skończone
import copy


class List_element:
    def __init__(self, el):
        self.data = copy.deepcopy(el)
        self.next = None


class List:
    def __init__(self):
        self.__head = None
        self.__length = 0

    def destroy(self):
        self.__head = None
        self.__length = 0

    def add(self, el):
        h = self.__head
        self.__head = List_element(el)
        self.__head.next = h
        self.__length += 1

    def is_empty(self):
        if not self.__length:
            return True
        else:
            return False

    def length(self):
        return self.__length

    def get(self):
        if self.__head is not None:
            return copy.deepcopy(self.__head.data)
        else:
            raise MemoryError("List is empty")

    def take(self, n: int):
        if n > self.__length:
            n = self.__length
        h = copy.deepcopy(self.__head)
        s = h
        for i in range(n):
            h = h.next
        h.next = None
        new_lst = List()
        new_lst.__head = s
        new_lst.__length = n
        return new_lst

    def drop(self, n: int):
        if n > self.__length:
            n = self.length()
        h = self.__head
        for i in range(n):
            h = h.next
        s = copy.deepcopy(h)
        new_lst = List()
        new_lst.__head = s
        new_lst.__length = self.__length - n
        return new_lst

    def remove(self):
        self.__head = self.__head.next
        self.__length -=1

    def __str__(self):
        h = self.__head
        st = ""
        for i in range(self.__length):
            st += str(h.data) + " "
            h = h.next
        return st

    def remove_last(self):
        h = self.__head
        while h.next is not None:
            h = h.next
        h = None
        self.__length -= 1

    def add_to_end(self, el):
        h = self.__head
        while h.next is not None:
            h = h.next
        h.next = List_element(el)
        self.__length += 1


ll = [('AGH', 'Kraków', 1919),
      ('UJ', 'Kraków', 1364),
      ('PW', 'Warszawa', 1915),
      ('UW', 'Warszawa', 1915),
      ('UP', 'Poznań', 1919),
      ('PG', 'Gdańsk', 1945)]
l = List()

for el in ll:
    l.add(el)
print("podstawowa lista:", l)
print("metoda get:", l.get())
l_add = copy.deepcopy(l)
l_add.add(("aaaa",'bbbb', 29))
print("lista po użyciu add:", l_add)
l_add.remove()
print("lista add po uzyciu remove: ", l_add)
l_take = l.take(3)
l_drop = l.drop(4)
print("lista zwracana metodą take: ",l_take, "długość:", l_take.length())
print("lista zwracana metodą drop: ",l_drop, "długość:", l_drop.length())
l_emp = l.take(0)
print("czy lista jest pusta (True):", l_emp.is_empty())
print("czy lista jest pusta (False):", l.is_empty())
print("usunięcie ostatniego elementu:")
print("przed:",l)
l.remove_last()
print("po:",l)
print("dodanie ostatniego elementu:")
print("przed:",l)
l.add_to_end(ll[5])
print("po:",l)
print("metoda get:", l.get())
print("Zniszczenie listy:")
l.destroy()
print(l, l.is_empty())
