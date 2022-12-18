#skończone
class Node:
    def __init__(self, key: int, data, left=None, right=None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        self.balance = 0


def search(key: int, node: Node):
    if node is None:
        return None
    if key == node.key:
        return node.data
    elif key < node.key:
        if node.left is None:
            return None
        else:
            return search(key, node.left)
    elif key > node.key:
        if node.right is None:
            return None
        else:
            return search(key, node.right)
    else:
        return None


def bottom_left(node):
    if node.left is None:
        return node
    else:
        return bottom_left(node.left)


def rotate_right(node):
    n = node.left
    node.left = n.right
    n.right = node
    return n


def rotate_left(node):
    n = node.right
    node.right = n.left
    n.left = node
    return n


def balance(node):
    if node.balance <= -2:
        if node.right.balance > 0:
            node.right = rotate_right(node.right)
        return rotate_left(node)
    elif node.balance >= 2:
        if node.left.balance < 0:
            node.left = rotate_left(node.left)
        return rotate_right(node)

def delete(key, node):
    if node is None:
        return None
    elif key < node.key:
        node.left = delete(key, node.left)
        if node.balance <= -2 or node.balance >= 2:
            node = balance(node)
    elif key > node.key:
        node.right = delete(key, node.right)
        if node.balance <= -2 or node.balance >= 2:
            node = balance(node)
    else:
        if node.left is None and node.right is None:
            return None
        elif node.left is None and node.right is not None:
            node = node.right
        elif node.left is not None and node.right is None:
            node = node.left
        else:
            # szukamy najmniejszego elementu w prawym ramieniu
            temp = bottom_left(node.right)
            # zamieniamy parametry i usuwamy w prawym ramieniu wzięty element (element ma maksymalnie jednego potomka)
            node.key = temp.key
            node.data = temp.data
            node.right = delete(temp.key, node.right)

    node.balance = height(node.left) - height(node.right)
    if node.balance <= -2 or node.balance >= 2:
        node = balance(node)

    return node


def height(node):
    if node is None:
        return 0
    ## gdy dochodzimy do Nona to wysokość jest równa 0, przy wracaniu inkrementujemy 1
    left_h = height(node.left)
    right_h = height(node.right)

    return max(left_h, right_h) + 1


def insert(key, data, node):
    if node == None:
        node = Node(key, data)
        return node
    if node.key == key:
        node.data = data
        return node
    if key < node.key:
        node.left = insert(key, data, node.left)
        node.balance = height(node.left) - height(node.right)
        if node.balance <= -2 or node.balance >= 2:
            node = balance(node)
        return node
    elif key > node.key:
        node.right = insert(key, data, node.right)
        node.balance = height(node.left) - height(node.right)
        if node.balance <= -2 or node.balance >= 2:
            node = balance(node)
        return node
    else:
        return node


def traverse_in_order(node, lst):
    if node is not None:
        traverse_in_order(node.left, lst)
        lst.append([node.key, node.data])
        traverse_in_order(node.right, lst)


class AVL():
    def __init__(self):
        self.root = None

    def search(self, key: int):
        return search(key, self.root)

    def insert(self, key: int, data):
        self.root = insert(key, data, self.root)

    def delete(self, key: int):
        self.root = delete(key, self.root)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def height(self):
        return height(self.root)

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.data)

            self._print_tree(node.left, lvl + 5)

    def print(self):
        lst = []
        traverse_in_order(self.root, lst)
        st = "{"
        for el in lst:
            st += str(el[0]) + ":" + str(el[1]) + ", "

        if len(st) > 1:
            st = st[:-2]
        st += "}"
        print(st)


tree = AVL()
D = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 2: 'E', 1: 'F', 11: 'G', 100: 'H', 7: 'I', 6: 'J', 55: 'K', 52: 'L', 51: 'M',
     57: 'N', 8: 'O', 9: 'P', 10: 'R', 99: 'S', 12: 'T'}
for i in D:
    tree.insert(i, D[i])
tree.print_tree()
tree.print()
print(tree.search(10))
tree.delete(50)
tree.delete(52)
tree.delete(11)
tree.delete(57)
tree.delete(1)
tree.delete(12)
tree.insert(3, "AA")
tree.insert(4, "BB")
tree.delete(7)
tree.delete(8)
tree.print_tree()
tree.print()