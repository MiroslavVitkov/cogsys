#!/usr/bin/env python3
# open file -> read lines -> create recursive tree -> crop weeds


'''Construct sentence tree from tokanised text or from a serialised tree.'''


def _get_first_child(string):
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

    # Return x, xs; brackets stripped.
    return string[first+1:last], string[last+1:]


def _get_head_tag(string):
    tag = string.split()[0]  # first word
    tag = tag[1:]  # remove initial '('
    return tag


def _split_into_children(string):
    # Identify between 0 and Inf children.
    children = []
    while True:
        child, string = _get_first_child(string)
        if(child):
            children.append(child)
        else:
            break

    return children


class Node:
    '''A tree of language tags.'''
    def __init__(self, tag, children=[]):
        self.tag = tag
        self.children = children

    def __repr__(self):
        return 'kur'



def build_tree(string):
    if not string:
        return None

    tag = _get_head_tag(string)
    children = _split_into_children(string)

    return Node(tag, children)


if __name__ == '__main__':
    print(build_tree('(S (NP (DT This) (NN time)) (, ,) (NP (DT the) (NNS firms)) (VP (VBD were) (ADJP (JJ ready))) (. .))'))
