import random


class Node:
    def __init__(self, val=()):
        self.left = None
        self.right = None
        self.data = val


def compare_nodes(a, b):
    return a - b


class Tree:
    def __init__(self):
        self.root = None

    def inorder_traversal(self, traversal, parent=None):
        parent = self.root if parent is None else parent
        return self.__inorder_traversal(parent, traversal)

    def __inorder_traversal(self, parent, traversal):
        if parent is None:
            return
        self.__inorder_traversal(parent.left, traversal)
        traversal.append(parent.data)
        self.__inorder_traversal(parent.right, traversal)

    def preorder_route(self, parent=None, nth=0, level=0):
        traversal = [self.root]
        parent = self.root if parent is None else parent

        self.__preorder_route(parent, traversal, nth, level)

        return traversal

    def __preorder_route(self, parent, traversal, nth=0, level=0):
        if parent is None:
            return

        traversal.append((parent, nth, level))

        self.__preorder_route(parent.left, traversal, nth - 1, level - 1)
        self.__preorder_route(parent.right, traversal, nth + 1, level - 1)


    def get_min(self, parent):
        left = None
        while parent.left:
            parent = parent.left

        return parent.data

    def get_depth(self, parent, level=0, max_level=0):
        if parent is None:
            if max_level and level > max_level:
                max_level = level
                return max_level
            return level

        max_level = self.get_depth(parent.left, level + 1, max_level)
        max_level = self.get_depth(parent.right, level + 1, max_level)

        if max_level and level > max_level:
            max_level = level
            return max_level

    def has_inner_children(self, node):
        return ((node.left and node.left.right) and (node.right and node.right.left)) is not None


class BST(Tree):
    def __init__(self):
        super().__init__()

    def generate(self, nodes):
        for n in nodes:
            if type(n) is tuple:
                self.insert(n[0], n[1])
            else:
                self.insert(n, None)

    def randomize(self, node_count=10, value_range=(0, 100)):
        for n in range(node_count):
            self.insert(random.Random().randint(value_range[0], value_range[1]), value="random")

    def insert(self, key: int, value=None):
        #print((key, value))

        return self.__insert(self.root, (key, value))

    def __insert(self, parent, val):
        if parent is None:
            parent = Node(val)
            parent.data = val
            if self.root is None:
                self.root = parent
                #print(f"Root: {parent.data}")
            return parent

        if compare_nodes(val[0], parent.data[0]) < 0:
            left = self.__insert(parent.left, val)
            if parent.left is None:
                parent.left = left
                # print(f"Left: {val} < {parent.data}")
                return left
        elif compare_nodes(val[0], parent.data[0]) > 0:
            right = self.__insert(parent.right, val)
            if parent.right is None:
                parent.right = right
                # print(f"Right: {val} > {parent.data}")
                return right
