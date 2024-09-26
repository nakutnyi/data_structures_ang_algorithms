"""
Red-black tree is a self-balancing binary search tree.
with a few additional constraints:
- Each node is either black or red.
- Root and leaves are always black.
- If a node is red, then its children are black.
- All paths from a node to its NIL descendants contain the same number of black nodes
"""
from termcolor import colored

from binary_search import BinarySearchTree

BLACK = True
RED = False


class MetaNil(type):
    """Just here to display Nil nicely"""
    def __str__(self):
        return colored("NIL",  "black")


class Nil(metaclass=MetaNil):
    """The empty leaf node"""
    color = BLACK


class Node:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.left = Nil
        self.right = Nil
        self.parent = None

    def __str__(self):
        out = str(self.value).zfill(3)
        return colored(out, "black") if self.color == BLACK else colored(out, "red")


class RedBlackTree(BinarySearchTree):
    """A kind of self-balancing binary search tree"""

    def __init__(self):
        self.root = None

    def link_new_top_to_its_new_parent(self, old_top, new_top):
        new_top.parent = old_top.parent
        if old_top is self.root:
            self.root = new_top
        elif old_top is old_top.parent.left:
            old_top.parent.left = new_top
        elif old_top is old_top.parent.right:
            old_top.parent.right = new_top

    def rotate_left(self, old_top):
        new_top = old_top.right

        old_top.right = new_top.left
        if new_top.left is not Nil:
            new_top.left.parent = old_top

        self.link_new_top_to_its_new_parent(old_top, new_top)

        new_top.left = old_top
        old_top.parent = new_top

    def rotate_right(self, old_top):
        new_top = old_top.left

        old_top.left = new_top.right
        if new_top.right is not Nil:
            new_top.right.parent = old_top

        self.link_new_top_to_its_new_parent(old_top, new_top)

        new_top.right = old_top
        old_top.parent = new_top

    def insert_and_fixup(self, value):
        """
        1. Insert a new node and color it red
        2. Rotate and recolor
        """
        new = Node(value, RED)

        # first scenario
        if not self.root:
            new.color = BLACK
            self.root = new
            return

        # just insert
        parent = None
        child = self.root

        while child is not Nil:
            if new.value > child.value:
                parent, child = child, child.right
            elif new.value < child.value:
                parent, child = child, child.left
        if new.value < parent.value:
            parent.left = new
            new.parent = parent
        elif new.value > parent.value:
            parent.right = new
            new.parent = parent

        self.fix_insert(new)

    @staticmethod
    def get_relatives(node):
        parent = node.parent
        grandparent = parent.parent

        return parent, grandparent

    def fix_insert(self, node):
        r"""
        The first scenario when new node is root is covered in the "insert" method
        Remaining three scenarios are covered here:

        2. New node's uncle is red - recolor


        3. New node's uncle is black (TRIANGLE scenario) - rotate and recolor:
             3.1                      3.2
          grandparent             grandparent
             / \                     / \
        uncle  parent     or    uncle  parent
                /                   \
            node                    node


        4. New node's uncle is black (LINE scenario) - rotate and recolor:
              4.1                    4.2
          grandparent             grandparent
             /  \                    / \
        uncle  parent     or     uncle  parent
                  \               /
                  node         node
        """

        while node != self.root and node.parent.color == RED:
            parent, grandparent = self.get_relatives(node)
            if parent == grandparent.right:
                uncle = grandparent.left
                if uncle.color == RED:  # case 2
                    uncle.color = BLACK
                    parent.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                elif uncle.color == BLACK:
                    if node is parent.left:  #                             ‾|
                        node = parent  #                                    |
                        parent, grandparent = self.get_relatives(node)  #    > # case 3.1
                        self.rotate_right(node)  #                          |
                    parent.color = BLACK  #                                 |  ‾|
                    grandparent.color = RED  #                              |    > # case 4.1
                    self.rotate_left(grandparent)  #                       _|  _|
            elif parent == grandparent.left:
                uncle = node.parent.parent.right

                if uncle.color == RED:  # case 2
                    uncle.color = BLACK
                    parent.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                elif uncle.color == BLACK:
                    if node == parent.right:  #                           ‾|
                        node = node.parent  #                              |
                        parent, grandparent = self.get_relatives(node)  #   > # case 3.2
                        self.rotate_left(node)  #                          |
                    parent.color = BLACK  #                                |  ‾|
                    grandparent.color = RED  #                             |    > # case 4.2
                    self.rotate_right(grandparent)  #                     _|  _|
        self.root.color = BLACK

    def display(self, node=None, last=True, header='', index=None):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        side = None
        if not node:
            node = self.root
        if index is None:
            side = ""
        elif index == 0:
            side = "left "
        elif index == 1:
            side = "right "
        row = header + (elbow if last else tee) + side + str(node)
        print(row)
        if node is not Nil:
            children = [node.left, node.right]
            for index, child in enumerate(children):
                self.display(
                    node=child,
                    header=header + (blank if last else pipe),
                    last=index == len(children) - 1,
                    index=index,
                )

    def delete(self, value):
        """
        Cases:
        1. Left child is Nil
        2. Right child is Nil
        3. Neither of children is Nil
        """
        node = self.search(value)

        if node == Nil:
            return "Key not found!"

        y = node
        y_orig_color = y.color

        # case 1
        if node.left == Nil:
            x = node.right
            self.transplant(node, node.right)
        # case 2
        elif node.right == Nil:
            x = node.left
            self.transplant(node, node.left)
        # case 3
        else:
            y = self.minimum(node.right)
            y_orig_color = y.color
            x = y.right

            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.p = y

            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_orig_color == BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                # type 1
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotate_left(x.parent)
                    w = x.parent.right
                # type 2
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    # type 3
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotate_right(w)
                        w = x.parent.right
                    # type 4
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                # type 1
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotate_right(x.parent)
                    w = x.parent.left
                # type 2
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    # type 3
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotate_left(w)
                        w = x.parent.left
                    # type 4
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = BLACK

    # O(1)
    def transplant(self, new_node, old_node):
        if new_node.parent is None:
            self.root = old_node
        elif new_node == new_node.parent.left:
            new_node.parent.left = old_node
        else:
            new_node.parent.right = old_node
        old_node.parent = new_node.parent

    @staticmethod
    def minimum(node):
        while node.left is not Nil:
            node = node.left
        return node


tree = RedBlackTree()
tree.insert_and_fixup(15)
tree.insert_and_fixup(5)
tree.insert_and_fixup(1)
tree.insert_and_fixup(2)
tree.insert_and_fixup(4)
tree.insert_and_fixup(7)
tree.insert_and_fixup(10)
tree.display()

tree.delete(5)
tree.display()