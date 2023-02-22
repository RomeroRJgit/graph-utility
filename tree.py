import random


class Node:
    def __init__(self, key, val=None):
        if val is None:
            val = {}
        self.data = (key, val)
        self.left = None
        self.right = None
        self.parent = None
        self.sibling = None
        self.index = 0
        self.depth = 0
        self.isSuccessor = False


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
        traversal = []
        parent = self.root if parent is None else parent

        traversal = self.__preorder_route(parent, traversal, nth, level)
        return traversal

    def __preorder_route(self, parent, traversal, index=0, level=0):
        if parent is None:
            return traversal

        traversal.append((parent, index, level))
        parent.index = index
        parent.level = level

        self.__preorder_route(parent.left, traversal, index - 1, level + 1)
        self.__preorder_route(parent.right, traversal, index + 1, level + 1)

        return traversal


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

    def is_inner(self, node):
        return node.parent and (node.parent.left is not None and node.parent.right is not None)


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
            self.insert(random.Random().randint(value_range[0], value_range[1]))

    def delete(self, key: int):
        node = self.search(key)
        print(f"n: {node}")

    def search(self, key: int):
        return self.__search(self.root, key)

    def __search(self, node, key: int):
        if key == node.data[0]:
            print(node)
            return node

        print(key)
        print(f"?: {node.data[0]}")
        if key < node.data[0]:
            self.__search(node.left, key)
        elif key > node.data[0]:
            self.__search(node.right, key)

        return node if node else None

    def insert(self, key: int, value=None):
        if value is None:
            value = {}

        #print(f"Inserting: {(key, value)}")
        return self.__insert(self.root, (key, value))

    def __insert(self, parent, data=(-1, {})):
        if parent is None:
            parent = Node(data[0], val=data[1])
            if self.root is None:
                self.root = parent
                print(f"Root: {parent.data}")
            return parent

        if compare_nodes(data[0], parent.data[0]) < 0:
            left = self.__insert(parent.left, data)
            if parent.left is None:
                parent.left = left
                print(f"Left: {data[0]} < {parent.data[0]}")
                parent.left.parent = parent
                if parent.right:
                    parent.left.sibling = parent.right
            return parent.left
        elif compare_nodes(data[0], parent.data[0]) > 0:
            right = self.__insert(parent.right, data)
            if parent.right is None:
                print(f"Right: {data[0]} > {parent.data[0]}")
                parent.right = right
                parent.right.parent = parent
                if parent.left:
                    parent.right.sibling = parent.left
            return parent.right
