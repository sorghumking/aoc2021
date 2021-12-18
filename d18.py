import unittest

class Node:
    def __init__(self, l, r, parent=None):
        self.l = l
        self.r = r
        self.parent = parent

    def root(self):
        return self.parent is None

def create_tree(num):
    root = parse(num)
    link(root)
    return root

# Create tree of nodes, not setting parents
def parse(num):
    if type(num) == list:
        l = parse(num[0])
        r = parse(num[1])
        return Node(l, r)
    else:
        return num

# Link children to their parents
def link(node, depth=0):
    if depth == 0:
        node.parent = None
    for n in [node.l, node.r]:
        if type(n) == Node:
            n.parent = node
            link(n, depth+1)

# return listified representation of tree
def dump(node):
    if type(node) == Node:
        return [dump(node.l), dump(node.r)]
    else:
        return node

# find next node to explode
def find_explode(node, depth=0):
    if type(node) == Node:
        if type(node.l) == int and type(node.r) == int and depth+1 > 4:
            return node
        for n in [node.l, node.r]:
            result = find_explode(n, depth+1)
            if result is not None:
                return result
    return None

# node: exploded node
# Find node to which we'll add exploded left value.
def find_left(node):
    p = node.parent
    cur_node = node
    while p is not None:
        if p.l != cur_node: # don't retrace steps
            if type(p.l) == int: 
                return p
            sub = p.l
            while True: # traverse down and to the right
                if type(sub.r) == int:
                    return sub
                sub = sub.r
        cur_node = p
        p = p.parent
    return None

def find_right(node):
    p = node.parent
    cur_node = node
    while p is not None:
        if p.r != cur_node:
            if type(p.r) == int:
                return p
            sub = p.r
            while True:
                if type(sub.l) == int:
                    return sub
                sub = sub.l
        cur_node = p
        p = p.parent
    return None

def explode(node):
    assert type(node.l) == int and type(node.r) == int
    lval, rval = node.l, node.r
    lnode = find_left(node)
    if lnode is not None:
        if type(lnode.r) == int:
            lnode.r += lval
        else:
            lnode.l += lval
    rnode = find_right(node)
    if rnode is not None:
        if type(rnode.l) == int:
            rnode.l += rval
        else:
            rnode.r += rval
    parent = node.parent
    if parent.l == node:
        parent.l = 0
    else:
        parent.r = 0

def split(node):
    for n in [node.l, node.r]:
        if type(n) == int:
            if n >= 10:
                newl, newr = n // 2, n // 2 + 1
                if n == node.l:
                    node.l = Node(newl, newr, node)
                elif n == node.r:
                    node.r = Node(newl, newr, node)
                return True
        else:
            if split(n):
                return True
    return False



class ExplodeTests(unittest.TestCase):
    def test_find_explode(self): # find next pair to explode
        tests = [
            ([[[[[9,8],1],2],3],4], [9,8]),
            ([7,[6,[5,[4,[3,2]]]]], [3,2]),
            ([[6,[5,[4,[3,2]]]],1], [3,2]),
            ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [7,3]),
            ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [3,2])
        ]
        for t, expected in tests:
            tree = create_tree(t)
            node = find_explode(tree, depth=0)
            self.assertEqual(dump(node), expected)

    def test_explode(self):
        tests = [
            ([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]),
            ([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]),
            ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
            ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
            ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]])
        ]
        for t, expected in tests:
            tree = create_tree(t)
            node = find_explode(tree)
            explode(node)
            self.assertEqual(dump(tree), expected)

    def test_split(self):
        tests = [
            ([[[[0,7],4],[15,[0,13]]],[1,1]], [[[[0,7],4],[[7,8],[0,13]]],[1,1]]),
            ([[[[0,7],4],[[7,8],[0,13]]],[1,1]], [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]),
            ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], [[[[0,7],4],[[7,8],[6,0]]],[8,1]]) # no split for this input
        ]
        for t, expected in tests:
            tree = create_tree(t)
            split(tree)
            self.assertEqual(dump(tree), expected)

if __name__ == "__main__":
    unittest.main()
    # tree = create_tree([[[[0,7],4],[15,[0,13]]],[1,1]])
    # split(tree)
    # print(dump(tree))
    # root = create_tree([[[[[9,8],1],2],3],4])
    # ex = find_explode(root)
    # explode(ex)
    # print(dump(root))

    # print(root == root)
    # print(root == parse([[[[9,8],1],2],3]))
    # link(root, depth=0)
    # ex = find_explode(root, depth=0)
    # print(dump(ex))
    # result = dump(root)
    # print(result)
