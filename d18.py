import math
import unittest

def parse_input(inputfile):
    numbers = []
    with open(inputfile) as f:
        for line in f.readlines():
            numbers.append(eval(line.strip()))
    return numbers

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

# node: exploded node
# Find node to which we'll add exploded right value.
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

# Explode node.
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

# If any value >= 10 split leftmost value and return True, else False.
def split(node):
    for n in [node.l, node.r]:
        if type(n) == int:
            if n >= 10:
                newl, newr = math.floor(n/2), math.ceil(n/2)
                if n == node.l:
                    node.l = Node(newl, newr, node)
                elif n == node.r:
                    node.r = Node(newl, newr, node)
                return True
        else:
            if split(n):
                return True
    return False

# Add node and new_node, return new root
def add(node, new_node):
    new_root = Node(node, new_node)
    node.parent = new_root
    new_node.parent = new_root
    return new_root

# Explode and split tree until fully reduced.
def reduce(tree):
    while True:
        node = find_explode(tree)
        if node is not None:
            explode(node)
            continue
        result = split(tree)
        if result:
            continue
        break

# Return magnitude of tree.
def magnitude(tree):
    if type(tree.l) == int and type(tree.r) == int:
        return 3*tree.l + 2*tree.r
    elif type(tree.l) == int:
        return 3*tree.l + 2*magnitude(tree.r)
    elif type(tree.r) == int:
        return 3*magnitude(tree.l) + 2*tree.r
    return 3*magnitude(tree.l) + 2*magnitude(tree.r)
    
def p1(snailfish_numbers):
    tree = create_tree(snailfish_numbers[0])
    for num in snailfish_numbers[1:]:
        tree_to_add = create_tree(num)
        tree = add(tree, tree_to_add)
        reduce(tree)
    print(f"Fully reduced sum: {dump(tree)}")
    print(f"Part 1: Magnitude = {magnitude(tree)}")

def magnitude_of_two(num1, num2):
    add1 = create_tree(num1)
    add2 = create_tree(num2)
    tree = add(add1, add2)
    reduce(tree)
    return magnitude(tree)

def p2(snailfish_numbers):
    seen = []
    max_magnitude = 0
    for idx1, num1 in enumerate(snailfish_numbers):
        for idx2, num2 in enumerate(snailfish_numbers):
            if idx1 == idx2:
                continue # don't add same number

            # first number + second number
            if (idx1, idx2) in seen:
                continue
            else:
                seen.append((idx1,idx2))
            mag = magnitude_of_two(num1, num2)
            if mag > max_magnitude:
                max_magnitude = mag
            
            # second number + first number
            if (idx2, idx1) not in seen:
                continue
            else:
                seen.append((idx2, idx1))
            mag = magnitude_of_two(num2, num1)
            if mag > max_magnitude:
                max_magnitude = mag
    print(f"Part 2: max magnitude for any pair is {max_magnitude}")


# Tests, so useful!
class ExplodeTests(unittest.TestCase):
    def test_find_explode(self):
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

    def test_add(self):
        tests = [
            ([[[[4,3],4],4],[7,[[8,4],9]]], [1,1], [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
        ]
        for t, addend, expected in tests:
            tree = create_tree(t)
            new_tree = create_tree(addend)
            new_root = add(tree, new_tree)
            self.assertEqual(dump(new_root), expected)

    def test_reduce(self):
        tests = [
            ([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]], [[[[0,7],4],[[7,8],[6,0]]],[8,1]])
        ]
        for t, expected in tests:
            tree = create_tree(t)
            reduce(tree)
            self.assertEqual(dump(tree), expected)

    def test_magnitude(self):
        tests = [
            ([[9,1],[1,9]], 129),
            ([[1,2],[[3,4],5]], 143),
            ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
            ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
            ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
            ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
            ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
            ([[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]], 3993)
        ]
        for t, expected in tests:
            tree = create_tree(t)
            self.assertEqual(magnitude(tree), expected)

if __name__ == "__main__":
    # unittest.main()
    snailfish_numbers = parse_input("inputs/d18.txt")
    p1(snailfish_numbers)
    p2(snailfish_numbers)
