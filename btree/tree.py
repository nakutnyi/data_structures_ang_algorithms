class Node:
    def __init__(self):
        self.values = []
        self.children = []
        self.is_leaf = True

    def insert(self, value):
        self.children.append(value)
        self.children.sort()

    def need_transform(self, degree) -> bool:
        return len(self.children) == degree

    def get_new_parent_index(self):
        length = len(self.children)

    def transform(self):
        pass

    def _get_child_index(self, value) -> int:
        i = 0
        while i < len(self.values):
            temp = self.values[i]
            if value >= temp:
                return i + 1
            i += 1
        return 0

    def get_child_by_value(self, value) -> 'Node':
        child_index = self._get_child_index(value)
        return self.children[child_index]


class BTree:
    def __init__(self, degree=3):
        self.degree = degree
        self.root = Node()

    def insert(self, value):
        node = self.root
        while not node.is_leaf:
            node = node.get_child_by_value(value)
        node.insert(value)
        if node.need_transform(self.degree):
            node.transform()


    def delete(self, value):
        pass

    def search(self, value):
        pass

