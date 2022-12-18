#skończone
import copy


############################################################
##interface
#############################################################

class List_element:
    def __init__(self):
        self.data = None
        self.next = None


def nil():
    return None


def cons(el, lst):
    new_lst = List_element()
    new_lst.data = copy.deepcopy(el)
    new_lst.next = lst
    return new_lst


def first(lst: List_element):
    if lst is not None:
        return copy.deepcopy(lst.data)
    else:
        raise AssertionError("List i empty, you can't take first element")


def rest(lst: List_element):
    if lst is not None:
        return lst.next
    else:
        return None


############################################################
##koniec interface'u
#############################################################

def create():
    return nil()


def destroy(lst):
    lst = None


def add(el, lst):
    return cons(el, lst)


def remove(lst):
    if not is_empty(lst):
        return rest(lst)
    else:
        return None


def get(lst):
    return first(lst)


def list_str(lst):
    st = "["
    while not is_empty(lst):
        st += " " + str(first(lst))
        lst = rest(lst)
    st += "]"
    return st


def is_empty(lst):
    if lst is None:
        return True
    else:
        return False


def length(lst):
    if is_empty(lst):
        return 0
    else:
        return 1 + length(rest(lst))


def add_end(el, lst):
    if is_empty(lst):
        return cons(el, lst)
    else:
        return cons(first(lst), add_end(el, rest(lst)))


def drop(n, lst):
    if n == 0:
        return lst
    return drop(n - 1, rest(lst))


## działanie podobne do add_end, tylko zatrzymujemy się gdy n == 0, a nie gdy lista jest pusta
def take(n, lst):
    if n == 0:
        return None
    recreated_lst = take(n - 1, rest(lst))
    return cons(first(lst), recreated_lst)


def remove_last(lst):
    if not is_empty(lst):
        return take(length(lst)-1, lst)
    else:
        return None


ll = [('AGH', 'Kraków', 1919),
      ('UJ', 'Kraków', 1364),
      ('PW', 'Warszawa', 1915),
      ('UW', 'Warszawa', 1915),
      ('UP', 'Poznań', 1919),
      ('PG', 'Gdańsk', 1945)]

l = create()  ## to to samo co head = None

for el in ll:
    l = add_end(el, l)

print(list_str(l))
print("funkcja get:", get(l))
l_add = add(("aaaa",'bbbb', 29), l)
print("po add",list_str(l_add))
l_add = remove(l_add)
print("po remove", list_str(l_add))
l_take = take(3, l)
print("po take dla 3 elementów", list_str(l_take))
l_drop = drop(3, l)
print("po drop dla 3 elementów", list_str(l_drop))
l_empty = create()
l_empty_take1 = take(0, l)
l_empty_take2 = take(1, l)
print("test czy pusta dla create():", is_empty(l_empty))
print("test czy pusta dla take(0, l):", is_empty(l_empty_take1))
print("test czy pusta dla take(1, l):", is_empty(l_empty_take2))
l_rem_last = remove_last(l)
print("lista pierwotna po użyciu remove_last", list_str(l_rem_last))
l_rem_last = add_end(ll[5], l_rem_last)
print("lista po użyciu remove_last i dodaniu spowrotem ostatniego elemantu:", list_str(l_rem_last))
l = destroy(l)
print("lista po destroy:", list_str(l), ", czy pusta:", is_empty(l))
