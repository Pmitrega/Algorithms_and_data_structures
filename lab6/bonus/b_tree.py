#skonczone
import copy
from typing import Union


class BTreeEl:
    def __init__(self, max_children, el):
        if max_children < 2:
            raise ValueError("max children cant be smaller than 2")
        self.keys = [None for i in range(max_children - 1)]
        self.children = [None for i in range(max_children)]
        self.keys[0] = el
        self.size = 1

    def __str__(self):
        return str(self.keys)

    def is_full(self, max_children):
        return self.size >= max_children - 1

    def __le__(self, other):
        if self.keys[0] < other.keys[0] and self.keys[self.size] < other.keys[0]:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.keys[0] > other.keys[other.size - 1]:
            return True
        else:
            return False


def is_leaf(node):
    return node.children[0] is None


def put_to_end(node, el, max_children):
    for i in range(max_children - 1):
        if node[i] is None:
            node[i] = el
            return
    raise AssertionError("node is full")


def split_leaf(node: BTreeEl, key, max_children):
    node = copy.deepcopy(node)
    node.keys.append(key)
    node.keys.sort()
    smaller_node_k = node.keys[:max_children // 2 - 1] + [None] * (max_children // 2)
    bigger_node_k = node.keys[max_children // 2:] + [None] * (max_children // 2 - 1)
    node_s = BTreeEl(4, None)
    node_b = BTreeEl(4, None)
    node_s.size = max_children // 2 - 1
    node_s.keys = smaller_node_k
    node_b.size = max_children // 2
    node_b.keys = bigger_node_k
    middle = node.keys[max_children // 2 - 1]
    return node_s, node_b, middle


def split_branch(node: BTreeEl, key, max_children):
    node.keys.append(key)
    node.keys.sort()
    smaller_node_k = node.keys[:max_children // 2 - 1] + [None] * (max_children // 2)
    bigger_node_k = node.keys[max_children // 2:] + [None] * (max_children // 2 - 1)
    smaller_node_ch = node.children[:max_children // 2] + [None] * (max_children // 2)
    bigger_node_ch = node.children[max_children // 2:] + [None] * (max_children // 2)
    node_s = BTreeEl(4, None)
    node_b = BTreeEl(4, None)
    node_s.size = max_children // 2 - 1
    node_s.keys = smaller_node_k
    node_s.children = smaller_node_ch
    node_b.children = bigger_node_ch
    node_b.size = max_children // 2
    node_b.keys = bigger_node_k
    middle = node.keys[max_children // 2 - 1]
    return node_s, node_b, middle


def insert(node: Union[BTreeEl, None], key, max_children):
    if node is None:
        return BTreeEl(max_children, key), None, None
    if is_leaf(node):
        if not node.is_full(max_children):
            for i in range(max_children - 1):
                if node.keys[i] is not None and key < node.keys[i]:
                    node.keys.insert(i, key)
                    node.keys.pop()
                    node.size += 1
                    return node, None, None
                elif node.keys[i] is None:
                    node.keys[i] = key
                    node.size += 1
                    return node, None, None
        else:
            node_s, node_b, middle = split_leaf(node, key, max_children)
            return node_s, node_b, middle
    elif not is_leaf(node):
        for i in range(max_children - 1):
            if node.keys[i] is not None and key < node.keys[i]:
                smaller, bigger, el = insert(node.children[i], key, max_children)
                if bigger is not None:
                    node.keys.insert(i, el)
                    node.keys.pop()
                    node.size += 1
                    node.children[i] = smaller
                    node.children.insert(i+1, bigger)
                    node.children.pop()
                return node, None, None
            elif node.keys[i] is None:
                smaller, bigger, el = insert(node.children[i], key, max_children)
                if bigger is not None:
                    node.keys.insert(i, el)
                    node.keys.pop()
                    node.size += 1
                    node.children.insert(i, None)
                    node.children[i] = smaller
                    node.children.insert(i+1, bigger)
                    node.children.pop()
                return node, None, None
            elif i == max_children - 2:
                smaller, bigger, el = insert(node.children[i + 1], key, max_children)
                if bigger is not None:
                    node.children.insert(i+1, smaller)
                    node.children.insert(i+2, bigger)
                    node.children.pop()
                    node.children.pop()
                    return split_branch(node, el, max_children)
                else:
                    node.children[i+1] = smaller
                    return node, None, None

    return node, None, None


class BTree:
    def __init__(self, max_children):
        if not max_children % 2:
            self.max_children = max_children
        else:
            raise ValueError("maximum number of children must be divided by 2")
        self.root = None

    def insert(self, key):
        smaller, bigger, middle = insert(self.root, key, self.max_children)
        if bigger is not None:
            self.root = BTreeEl(self.max_children, middle)
            self.root.children[0] = smaller
            self.root.children[1] = bigger
        else:
            self.root = smaller

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size + 1):
                if i < len(node.children):
                    self._print_tree(node.children[i], lvl + 1)
                if i < node.size:
                    print(lvl * '  ', node.keys[i])

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")




tree = BTree(4)
lst = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18 , 15, 10, 19]
for i in lst:
    tree.insert(i)
tree.print_tree()

tree2 = BTree(4)
for i in range(20):
    tree2.insert(i)
tree2.print_tree()

for i in range(20, 200):
    tree2.insert(i)
tree2.print_tree()

tree6ch = BTree(6)
for i in range(0, 200):
    tree6ch.insert(i)
tree6ch.print_tree()
