"""
Red-black tree is a self-balancing binary search tree.
with a few additional constraints:
- Each node is either black or red.
- Root and leaves are always black.
- If a node is red, then its children are black.
- All paths from a node to its NIL descendants contain the same number of black nodes
"""


class MetaNil(type):
    """Just here to display Nil nicely"""
    def __str__(self):
        return "NIL black"


class Nil(metaclass=MetaNil):
    """The empty leaf node"""
    red = False


class Node:
    def __init__(self, value, color):
        self.value = value
        self.red = color == "red"
        self.left = Nil
        self.right = Nil
        self.parent = None

    def __str__(self):
        return f"{str(self.value).zfill(3)} {'red' if self.red else 'black'}"


class RedBlackTree:
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

    def search(self):
        pass

    def insert(self, value):
        """
        1. Insert a new node and color it red
        2. Rotate and recolor
        """
        new = Node(value, "red")

        # first scenario
        if not self.root:
            new.red = False
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

    def fix_insert(self, new_node):
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

        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                uncle = new_node.parent.parent.left
                if uncle.red:  # case 2
                    uncle.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:      #  ‾|
                        new_node = new_node.parent            #    > # case 3.1
                        self.rotate_right(new_node)           #   |
                    new_node.parent.red = False               #   |  ‾|
                    new_node.parent.parent.red = True         #   |    > # case 4.1
                    self.rotate_left(new_node.parent.parent)  #  _|  _|
            else:
                uncle = new_node.parent.parent.right

                if uncle.red:  # case 2
                    uncle.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:      #  ‾|
                        new_node = new_node.parent             #    > # case 3.2
                        self.rotate_left(new_node)             #   |
                    new_node.parent.red = False                #   |  ‾|
                    new_node.parent.parent.red = True          #   |    > # case 4.2
                    self.rotate_right(new_node.parent.parent)  #  _|  _|
        self.root.red = False

    def display(self, node=None, last=True, header='', index=None):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
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
                self.display(node=child, header=header + (blank if last else pipe), last=index == len(children) - 1, index=index)

    def remove(self):
        pass


tree = RedBlackTree()
tree.insert(15)
tree.insert(5)
tree.insert(1)
tree.insert(2)
tree.insert(4)
tree.insert(7)
tree.insert(10)
tree.display()
