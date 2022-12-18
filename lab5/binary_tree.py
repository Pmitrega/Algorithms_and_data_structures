#skończone
class Node:
    def __init__(self, key: int, data, left=None, right=None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right


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




def delete(key, node):
    if node is None:
        return None
    elif key < node.key:
        node.left = delete(key, node.left)
    elif key > node.key:
        node.right = delete(key, node.right)
    else:
        if node.left is None and node.right is None:
            return None
        elif node.left is None and node.right is not None:
            t = node.right
            node = None
            return t
        elif node.left is not None and node.right is None:
            t = node.left
            node = None
            return t
        # szukamy najmniejszego elementu w prawym ramieniu
        temp = bottom_left(node.right)
        # zamieniamy parametry i usuwamy w prawym ramieniu wzięty element (element ma maksymalnie jednego potomka)
        node.key = temp.key
        node.data = temp.data
        node.right = delete(temp.key, node.right)

    return node


def height(node):
    if node is None:
        return 0
    ## gdy dochodzimy do Nona to wysokość jest równa 0, przy wracaniu inkrementujemy 1
    left_h = height(node.left)
    right_h = height(node.right)

    return max(left_h, right_h) + 1


def insert(key, data, node):
    if node is None:
        node = Node(key, data)
    elif key == node.key:
        node.data = data

    elif key < node.key:
        if node.left is None:
            node.left = Node(key, data)
        else:
            insert(key, data, node.left)
    elif key > node.key:
        if node.right is None:
            node.right = Node(key, data)
        else:
            insert(key, data, node.right)

    return node


def traverse_in_order(node, lst):
    if node is not None:
        traverse_in_order(node.left, lst)
        lst.append([node.key, node.data])
        traverse_in_order(node.right, lst)


class BST:
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


tree = BST()
D = {50:'A', 15:'B', 62:'C', 5:'D', 20:'E', 58:'F', 91:'G', 3:'H', 8:'I', 37:'J', 60:'K', 24:'L'}
for key in D:
    tree.insert(key, D[key])
#
tree.print_tree()
tree.print()
print(tree.search(24))
tree.insert(20, "AA")
tree.insert(6, "M")
tree.delete(62)
tree.insert(59, 'N')
tree.insert(100,' P')
tree.delete(8)
tree.delete(15)
tree.insert(55,' R')
tree.delete(50)
tree.delete(5)
tree.delete(24)
print(tree.height())
tree.print()
tree.print_tree()
