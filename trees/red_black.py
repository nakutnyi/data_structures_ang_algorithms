"""
Red-black tree is a self-balancing binary search tree.
with a few additional constraints:
- Each node is either black or red.
- Root and leaves are always black.
- If a node is red, then its children are black.
- All paths from a node to its NIL descendants contain the same number of black nodes
"""


BLACK = True
RED = False


class MetaNil(type):
    """Just here to display Nil nicely"""
    def __str__(self):
        return "NIL black"


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
        return f"{str(self.value).zfill(3)} {'red' if self.color == RED else 'black'}"


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

    def insert(self, value):
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

        while new_node != self.root and new_node.parent.color == RED:
            if new_node.parent == new_node.parent.parent.right:
                uncle = new_node.parent.parent.left
                if uncle.color == RED:  # case 2
                    uncle.color = BLACK
                    new_node.parent.color = BLACK
                    new_node.parent.parent.color = RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:      #  ‾|
                        new_node = new_node.parent            #    > # case 3.1
                        self.rotate_right(new_node)           #   |
                    new_node.parent.color = BLACK             #   |  ‾|
                    new_node.parent.parent.color = RED        #   |    > # case 4.1
                    self.rotate_left(new_node.parent.parent)  #  _|  _|
            else:
                uncle = new_node.parent.parent.right

                if uncle.color == RED:  # case 2
                    uncle.color = BLACK
                    new_node.parent.color = BLACK
                    new_node.parent.parent.color = RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:      #  ‾|
                        new_node = new_node.parent             #    > # case 3.2
                        self.rotate_left(new_node)             #   |
                    new_node.parent.color = BLACK                #   |  ‾|
                    new_node.parent.parent.color = RED          #   |    > # case 4.2
                    self.rotate_right(new_node.parent.parent)  #  _|  _|
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

            if y.p == node:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.p = y

            self.transplant(node, y)
            y.left = node.left
            y.left.p = y
            y.color = node.color

        if y_orig_color == BLACK:
            self.delete_fixup(x)

    # O(logn)
    def delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.p.left:
                w = x.p.right
                # type 1
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.rotate_left(x.p)
                    w = x.p.right
                # type 2
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    # type 3
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotate_right(w)
                        w = x.p.right
                    # type 4
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self.rotate_left(x.p)
                    x = self.root
            else:
                w = x.p.left
                # type 1
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.rotate_right(x.p)
                    w = x.p.left
                # type 2
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    # type 3
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotate_left(w)
                        w = x.p.left
                    # type 4
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self.rotate_right(x.p)
                    x = self.root
        x.color = BLACK

    # O(1)
    def transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

        # O(h) = O(logn) for RB trees

    def minimum(self, x):
        while x.left != Nil:
            x = x.left
        return x

    # O(h) = O(logn) for RB trees
    def search(self, k):
        x = self.root
        while x != Nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x


tree = RedBlackTree()
tree.insert(15)
tree.insert(5)
tree.insert(1)
tree.insert(2)
tree.insert(4)
tree.insert(7)
tree.insert(10)
tree.display()
