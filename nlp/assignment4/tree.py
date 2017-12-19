#!/usr/bin/env python3
# open file -> read lines -> create recursive tree
# -> cropweeds

'''Construct sentence tree from tokanised text or from a serialised tree.'''


def _extract_one_node(string):
    # Identify first opening bracket.
    try:
        first = string.index('(')
    except:
        return '', ''

    # Identify the matching closing bracket.
    last = None
    depth = 1
    for i in range(first+1, len(string)):
        if string[i] == '(':
            depth += 1
        elif string[i] == ')':
            depth -= 1
        if depth == 0:
            last = i
            break

    # Return x, xs, brackets stripped.
    return string[first+1:last], string[last+1:]





import re
from collections import defaultdict


def read(fname):
    '''Read a parse tree file into a string.'''
    with open(fname, 'r') as f:
        return [l for l in f.readlines()]


# Utilize autovivification.
def tree(): return defaultdict(tree)



def _deserialize(serial):
    if not serial:
        return None

    node = None
    value = serial.pop()
    if value != 'x':
        node = Node(value)
        node.left = _deserialize(serial)
        node.right = _deserialize(serial)
    return node


class Node:
    '''A tree of language tags.'''
    def __init__(self, tag, children=[]):
        self.tag = tag
        self.children = children

    def __repr__(self):
        children_repr = ",".join(repr(child) for child in self.children)
        return 'Node({.value},[{}])'.format(self, children_repr)

    @staticmethod
    def deserialize(string):
        '''Example input: `( (NP (NNP NCNB) (NNP Corp) (. .)) )`'''
        # Strip root node markings.
        stripped = string[3:-2]

        # Identify the tag name, whih is our node's value.
        tag = stripped.split()[0]

        # Identify between 0 and Inf children.
        children = []
        while True:
            child, rest = _extract_one_node(stripped)
            if(child):
                children.append(child)
                stripped = rest
            else:
                break

        return tag, children



if __name__ == '__main__':
    print(Node.deserialize('( (S (NP (DT This) (NN time)) (, ,) (NP (DT the) (NNS firms)) (VP (VBD were) (ADJP (JJ ready))) (. .)) )'))
