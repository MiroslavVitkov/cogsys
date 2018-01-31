#!/usr/bin/env python3


from nltk.data import load
from nltk.grammar import FeatureGrammar
from nltk.sem.util import interpret_sents


def extend_grammar(g, p):
    '''Extend a FeatureGrammar object with a new (string represented) production.'''
    start = g._start
    old = g._productions
    new = FeatureGrammar.fromstring(p)._productions
    ret = FeatureGrammar(start, old + new)
    return ret


def parse(g, s):
    '''Using a grammar, produce frоm a sentence a first order logic representation.'''
    results = interpret_sents([s], g, semkey='SEM')
    return [semrep for r in results for (synrep, semrep) in r]


def main():
    grammar = load('grammars/sample_grammars/sem2.fcfg')
    grammar = extend_grammar(grammar, r"N[NUM='sg', SEM=<\x.god(x)>] -> 'god'")
    sem = parse(grammar, 'Mary chases a god')
    print(sem)
    #print(extend_grammar(grammar, 'V -> N'))


if __name__ == '__main__':
    main()
