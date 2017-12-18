#!/usr/bin/env python3
# open file -> read lines -> create recursive tree
# -> cropweeds

'''Construct sentence tree from tokanised text or from a serialised tree.'''


import re
from collections import defaultdict


def read(fname):
    '''Read a parse tree file into a string.'''
    with open(fname, 'r') as f:
        return [l for l in f.readlines()]





# Utilize autovivification.
def tree(): return defaultdict(tree)


def _on_open_bracket():  # create new node
    pass


def _on_close_bracket():  # end something
    pass


# depth = 0
# on open bracket, depth++, create new node
# on close bracket, dept--


def deserialize():
    '''Read a tree from a file in the format ( (NP (NNP NCNB) (NNP Corp) (. .)) )'''
    with open(fname, 'r') as f:
        for l in f.readlines():
            pass

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
#(TOP (NP (NNP ARNOLD) (NNP ADVERTISING) (: :)))
#( (NP (NN Ad) (NNS Notes) (: ...) (. .)) )

        # One approach would be to procedurally loop through the input string,
        # keeping a pointer where the next nood needs to be inserted,
        # building the tree bottom-up, left to right.
        # For no particular reason, we decide to instead use a functional approach,
        # where each subtree is recursively passed the substring that describes it.
        return eval(string.replace("#", "()").replace("(", "Node("))

    @staticmethod
    def deserialize(string):
        '''Example input: `( (NP (NNP NCNB) (NNP Corp) (. .)) )`'''
#(TOP (NP (NNP ARNOLD) (NNP ADVERTISING) (: :)))
#( (NP (NN Ad) (NNS Notes) (: ...) (. .)) )

        # Recursively and immutably construct the tree bottom-up.
        from itertools import islice
        string = '( (NP (NN Ad) (NNS Notes) (: ...) (. .)) )'
        it = islice(string, 0, len(string))
        for 
        return string[2:15]
        # construct children first:
        # strip first and last bracket
        # identify tag, children
        
        # descend into children

if __name__ == '__main__':
    print(Node.deserialize('kurskapaci'))
