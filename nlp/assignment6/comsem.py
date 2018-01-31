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
    g = load('grammars/sample_grammars/sem2.fcfg')

    g = extend_grammar(g, r"N[NUM='sg', SEM=<\x.story(x)>] -> 'story'")

    g = extend_grammar(g, r"TV[NUM='sg', SEM=<\X y.X(\x.\z.tell(y,x,z))>, TNS='pres'] -> 'tells'")
    g = extend_grammar(g, r"TV[NUM='pl', SEM=<\X y.X(\x.\z.tell(y,x,z))>, TNS='pres'] -> 'tell'")

    g = extend_grammar(g,
     r"VP[NUM=?n, SEM=<?v(?obj1, ?obj2)>] -> TV[NUM=?n, SEM=?v] NP[SEM=?obj1] NP[SEM=?obj2]")

    sem = parse(g, 'Mary tells Suzie a story')
    print(sem)


if __name__ == '__main__':
    main()
