#!/usr/bin/env python3

'''
Usage: cyk "sentence"

Produces all possible parse trees for a string, given grammar GRAMMAR_FILE.
Source: https://en.wikipedia.org/wiki/CYK_algorithm

Firstly, a Chomsky normal form grammar is read in from a file.
Then, for each given string, words (terminals) are replaced
with tags (nonterminals), according to the grammar.
Then those terminals are combined according to the grammar,
producing all possible parse trees.
'''


import itertools
import numpy as np


GRAMMAR_FILE = "res/atis-grammar-cnf.cfg"
START_TAG = 'SIGMA'


def read_cnf_grammar(fname):
    '''fname - Chomsky normal form grammar.'''
    term0 = term1 = []
    nonterm0 = nonterm1 = nonterm2 = []
    with open(fname, 'r') as f:
        for l in f.readlines():
            s = l.split()
            if s[2][0] == '"':
                # Unary rule - nonterm -> "term"
                term0.append(s[0])
                term1.append(s[2][1:-1])
            else:
                # Binary rule - nonterm -> nonterm1 nonterm2
                nonterm0.append(s[0])
                nonterm1.append(s[2])
                nonterm2.append(s[3])
    return (term0, term1, nonterm0, nonterm1, nonterm2)


def tags_to_indices(grammar):
    '''Replace each tag string with a number.'''
    # Construct an ordered container of unique exhaustive set of tags.
    print('Determinig unique tags...')
    tags = set(grammar[0])
    tags.update(grammar[2])
    tags = list(tags)

    def tag_to_idx(tag):
        for i, v in enumerate(tags):
            if(v == tag):
                return i

    def tags_to_ids(iterable):
        return list(map(tag_to_idx, iterable))

    print('Converting strings to integers...')
    g0 = tags_to_ids(grammar[0])
    g2 = tags_to_ids(grammar[2])
    g3 = tags_to_ids(grammar[3])
    g4 = tags_to_ids(grammar[4])

    # All tag strings are replaced with integers.
    return (g0, grammar[1], g2, g3, g4), tags


def words_to_tags(grammar, sentence):
    '''Replace each word in `string` with a set of possible tags.'''
    # We are using space as a separator - make sure punctuation is recognised.
    for punct in '.,!?':
        sentence = sentence.replace(punct, ' ' + punct)

    to_tags = []
    for word in sentence.lower().split():
        tags = [grammar[0][i] for i, x in enumerate(grammar[1]) if x == word]
        to_tags.append(set(tags))
    print('Preterminals identified:', to_tags)
    return to_tags


def make_chart(grammar, sentence):
    '''Implement CYK parsing algorithm.'''
    print('Replacing tag strings with integers...')
    grammar, tags = tags_to_indices(grammar)
    print('Converting words to preterminal tags...')
    preterms = words_to_tags(grammar, sentence)
    chart = np.zeros((len(preterms), len(preterms), len(tags)), dtype=bool)

    # Zeroeth chart row.
    for word_index, p in enumerate(preterms):
        for tag_index in p:
            chart[0, word_index, tag_index] = True

    # Iterative step.
    for l in range(2, len(preterms)):  # Length of span.
        print('l =', l)
        for s in range(0, len(preterms)-l):  # Start of span.
            for p in range(1, l-1):  # Partition of span.
                for lhs, rhs0, rhs1 in zip(grammar[2], grammar[3], grammar[4]):
                    if(chart[p,s,rhs0] and chart[l-p, s+p, rhs1]):
                        print('Found tag', t, 'in position', l, s)
                        chart[l,s,t] = True

    return chart, tags


def is_in_grammar(sentence, fname=GRAMMAR_FILE):
    print('Reading grammar...')
    grammar = read_cnf_grammar(fname)
    print('Making chart...')
    chart, tags = make_chart(grammar, sentence)
    print('Inspecting result...')
    start = [i for i, v in enumerate(tags) if v == START_TAG]
    return start in chart[-1,0]


if __name__ == '__main__':
    import sys
    print(is_in_grammar(sys.argv[1]))
