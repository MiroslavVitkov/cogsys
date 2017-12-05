#!/usr/bin/env python3

'''
Usage: cyk "sentence"
Produces all possible parse trees for a string, given grammar GRAMMAR_FILE.
'''


import itertools


GRAMMAR_FILE = "res/atis-grammar-cnf.cfg"
START_TAG = 'SIGMA'


def read_cnf_grammar(fname):
    '''
    fname - Chomsky normal form grammar.
    '''
    term0 = []
    term1 = []
    nonterm0 = []
    nonterm1 = []
    nonterm2 = []
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


def preprocess(string):
    '''We are using space as a separator - make sure punctuation is recognised'''
    for punct in '.,!?':
        string = string.replace(punct, ' ' + punct)
    return string


def terms_to_preterms(preterms, terms, string):
    '''Replace each word in `string` with a set of possible tags.'''
    # step 0 - discard terminals
    parse_tree = []
    for word in preprocess(string).lower().split():
        tags = [preterms[i] for i, x in enumerate(terms) if x == word]
        parse_tree.append(set(tags))
    return parse_tree


def derive(nonterms0, nonterms1, nonterms2, preterms):
    '''Do one iteration of deriving tags. Resulting list is 1 item shorter.'''
    # step 1 -  consider word sequences of length 2 - this does not require hystory
    rules_rhs = list(zip(nonterms1, nonterms2))
    ret = []
    for d in zip(preterms, preterms[1:]):
        ret.append(set())
        for c in itertools.product(d[0], d[1]):
            [ret[-1].add(nonterms0[i]) for i, r in enumerate(rules_rhs) if c == r]
    return ret


def step2(nonterms0, nonterms1, nonterms2, preterms, nonterms)):
    # step 2 -  consider word sequences of length 3
    rules_rhs = list(zip(nonterms1, nonterms2))
    ret = []
    #ret.append(preterms[0] - nonterm[1]; preterms[1] - nonterm[0])
    #ret.append(preterms[1] - nonterm[2]; preterms[2] - nonterm[1])
    #ret.append(preterms[2] - nonterm[3]; preterms[3] - nonterm[2])

    for d in itertools.chain(zip(preterms, nonterms[1:], zip(nonterms[1:], preterms[1:])):
        ret.append(set())
        for c in itertools.product(d[0], d[1]):
            [ret[-1].add(nonterms0[i]) for i, r in enumerate(rules_rhs) if c == r]
    return ret


def step3(nonterms0, nonterms1, nonterms2, preterms, nonterms, currents)):
    # step 2 -  consider word sequences of length 4
    rules_rhs = list(zip(nonterms1, nonterms2))
    ret = []
    #ret.append(preterms[0] - nonterm[1]; preterms[1] - nonterm[0])
    #ret.append(preterms[1] - nonterm[2]; preterms[2] - nonterm[1])
    #ret.append(preterms[2] - nonterm[3]; preterms[3] - nonterm[2])

    for d in itertools.chain(zip(preterms, nonterms[1:], zip(nonterms[1:], preterms[1:])):
        ret.append(set())
        for c in itertools.product(d[0], d[1]):
            [ret[-1].add(nonterms0[i]) for i, r in enumerate(rules_rhs) if c == r]
    return ret



def parse(grammar, string):
    tree = []  # first row is unigraphs, second row is digraphs etc.
    row = terms_to_preterms(grammar[0], grammar[1], string)
    while(len(row) > 1):
        tree.append(row)
        row = derive(grammar[2], grammar[3], grammar[4], tree)
    return row


def is_in_grammar(string, fname=GRAMMAR_FILE):
    grammar = read_cnf_grammar(fname)
    head_cell = parse(grammar, string)
    if START_TAG in head_cell:
        return True
    else:
        return False


class CYKParser:
    def __init__(vikings, grammar=GRAMMAR_FILE):
        vikings._grammar = read_cnf_grammar(grammar)
        vikings._rules_rhs = list(zip(grammar[-2], grammar[-1]))


    def parse(vikings, sentence):
        pass


if __name__ == '__main__':
    import sys
    print(is_in_grammar(sys.argv[1]))
