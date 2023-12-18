"""
Binary search tree.
"""
from termcolor import colored


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


class BinarySearchTree:
    """A kind of self-balancing binary search tree"""

    def __init__(self):
        self.root = None

    # def display(self, node=None, last=True, header='', index=None):
    #     elbow = "└──"
    #     pipe = "│  "
    #     tee = "├──"
    #     blank = "   "
    #     side = None
    #     if not node:
    #         node = self.root
    #     if index is None:
    #         side = ""
    #     elif index == 0:
    #         side = "left "
    #     elif index == 1:
    #         side = "right "
    #     row = header + (elbow if last else tee) + side + str(node)
    #     print(row)
    #     if node is not Nil:
    #         children = [node.left, node.right]
    #         for index, child in enumerate(children):
    #             self.display(
    #                 node=child,
    #                 header=header + (blank if last else pipe),
    #                 last=index == len(children) - 1,
    #                 index=index,
    #             )

    def search(self, value):
        current_node = self.root
        while current_node is not Nil and value != current_node.value:
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return current_node
